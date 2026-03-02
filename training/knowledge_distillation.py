"""
This script contains an example how to extend an existent sentence embedding model to new languages.

Given a (monolingual) teacher model you would like to extend to new languages, which is specified in the teacher_model_name
variable. We train a multilingual student model to imitate the teacher model (variable student_model_name)
on multiple languages.

For training, you need parallel sentence data (machine translation training data). You need tab-seperated files (.tsv)
with the first column a sentence in a language understood by the teacher model, e.g. English,
and the further columns contain the according translations for languages you want to extend to.

This scripts downloads automatically the parallel sentences corpus. This corpus contains transcripts from
talks translated to 100+ languages. For other parallel data, see get_parallel_data_[].py scripts

Further information can be found in our paper:
Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation
https://huggingface.co/papers/2004.09813
"""

import logging
import traceback
from datetime import datetime

import numpy as np
from datasets import DatasetDict, load_dataset, concatenate_datasets

from sentence_transformers import LoggingHandler, SentenceTransformer, models
from sentence_transformers.evaluation import (
    EmbeddingSimilarityEvaluator,
    MSEEvaluator,
    SequentialEvaluator,
    TranslationEvaluator,
)
from sentence_transformers.losses import MSELoss
from sentence_transformers.trainer import SentenceTransformerTrainer
from sentence_transformers.training_args import SentenceTransformerTrainingArguments

import sys

from transformers import AutoModelForMaskedLM

from post_processing import whitening


def train(teacher_model_name, student_model_name, whiten, output_dir, num_epochs, grc_lat_dataset):

    logging.basicConfig(
        format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO, handlers=[LoggingHandler()]
    )
    logger = logging.getLogger(__name__)



    train_batch_size = 64
    inference_batch_size = 64



    # Here we define our SentenceTransformer teacher model.
    teacher_model = SentenceTransformer(teacher_model_name)
    logging.info(f"Teacher model: {teacher_model}")

    # Here we define our SentenceTransformer student model. If not already a Sentence Transformer model, it will do mean-pooling
    student_model = SentenceTransformer(student_model_name)
    if student_model_name=="cis-lmu/glot500-base":
        transformer = models.Transformer("cis-lmu/glot500-base")
        pooling = models.Pooling(transformer.get_word_embedding_dimension(), pooling_mode="mean")
        normalize = models.Normalize()
        student_model = SentenceTransformer(modules=[transformer, pooling, normalize])
    if student_model_name=="bowphs/SPhilBerta":
        normalize = models.Normalize()
        new_modules = list(student_model.children()) + [normalize]
        student_model = SentenceTransformer(modules=new_modules)
    logging.info(f"Student model: {student_model}")

    train_dataset = load_dataset("csv", data_files="grc_lat_dataset.csv", column_names=["non_english", "english"], split="train")
    if grc_lat_dataset=="False":
        train_dataset = load_dataset("csv", data_files="grc_eng_training_big.csv",
                                     column_names=["non_english", "english"], split="train")
        lat_eng_dataset = load_dataset("grosenthal/latin_english_translation")
        cols = lat_eng_dataset["train"].column_names
        cols_to_remove = [cols[0], cols[-1]]
        lat_eng_dataset = lat_eng_dataset.remove_columns(cols_to_remove)
        lat_eng_dataset = lat_eng_dataset.rename_column("en", "english")
        lat_eng_dataset = lat_eng_dataset.rename_column("la", "non_english")
        train_dataset = concatenate_datasets([train_dataset, lat_eng_dataset["train"]])
    train_dataset = train_dataset.shuffle(42)
    eval_dataset = load_dataset("csv", data_files="eval_dataset.csv", column_names=["greek", "latin"], split="train")

    # We want the student EN embeddings to be similar to the teacher EN embeddings and
    # the student non-EN embeddings to be similar to the teacher EN embeddings
    def prepare_dataset(batch):
        return {
            "english": batch["english"],
            "non_english": batch["non_english"],
            "label": teacher_model.encode(batch["english"], batch_size=inference_batch_size, show_progress_bar=False),
        }
    if whiten=="True":
        latin_embeddings = teacher_model.encode(
            train_dataset["english"],
            batch_size=inference_batch_size,
            convert_to_numpy=True
        )
        greek_embeddings = teacher_model.encode(
            train_dataset["non_english"],
            batch_size=inference_batch_size,
            convert_to_numpy=True
        )
        pooled_embeddings = np.vstack([latin_embeddings, greek_embeddings])

        transformed_embeddings = whitening(pooled_embeddings)
        num_latin = len(latin_embeddings)
        lat_whitened = transformed_embeddings[:num_latin]
        train_dataset = train_dataset.add_column("label", lat_whitened.tolist())
    else:
        train_dataset = train_dataset.map(prepare_dataset, batched=True, batch_size=inference_batch_size)

    train_loss = MSELoss(model=student_model)

    evaluators = []

    # Mean Squared Error (MSE) measures the (euclidean) distance between teacher and student embeddings
    dev_mse = MSEEvaluator(
        source_sentences=eval_dataset["latin"],
        target_sentences=eval_dataset["greek"],
        name="grc-lat",
        teacher_model=teacher_model,
        batch_size=inference_batch_size,
    )
    evaluators.append(dev_mse)

    # TranslationEvaluator computes the embeddings for all parallel sentences. It then check if the embedding of
    # source[i] is the closest to target[i] out of all available target sentences
    dev_trans_acc = TranslationEvaluator(
        source_sentences=eval_dataset["latin"],
        target_sentences=eval_dataset["greek"],
        name="grc-lat",
        batch_size=inference_batch_size,
    )
    evaluators.append(dev_trans_acc)

    evaluator = SequentialEvaluator(evaluators, main_score_function=lambda scores: np.mean(scores))

    # Define the training arguments
    args = SentenceTransformerTrainingArguments(
        output_dir=output_dir,
        num_train_epochs=int(num_epochs),
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=train_batch_size,
        fp16=False,
        save_strategy="epoch",
        logging_strategy="steps",
        logging_steps=50,
        logging_dir="logs",
        eval_strategy="steps",
        eval_steps=50,
        warmup_ratio=0.1,
        logging_first_step=True,
        save_total_limit=1,
        remove_unused_columns=False,
        report_to='none'
    )

    # Create the trainer & start training
    trainer = SentenceTransformerTrainer(
        model=student_model,
        args=args,
        train_dataset=train_dataset,
        loss=train_loss,
        evaluator=evaluator
    )
    trainer.train()

    # Save the trained & evaluated model locally
    final_output_dir = output_dir
    student_model.save(final_output_dir)

if __name__ == '__main__':
    train(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
