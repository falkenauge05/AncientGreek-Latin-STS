# Training Models

## Fine-tuning (training.py)

This is for training with parallel sentences (Ancient Greek-Latin).
You need a training.csv file with the corresponding parallel data in the directory.
Then you can specify the model you want to train here:

    model = SentenceTransformer("bowphs/SPhilBerta", device="cuda")

The output_directory has to be specified at two locations:

    args = SentenceTransformerTrainingArguments(
        output_dir='sphilberta_unpr_big',

and
    
    trainer.save_model("sphilberta_unpr_big")

To start the training process, just execute:

    python training.py

If you want to train a word-level model at the eighth layer, uncomment the code block
at the top of the file and specify model name and layer number accordingly.


## Knowledge Distillation

Execute the following command with the respecting information:

    python knowledge_distillation.py teacher_model_name student_model_name whiten(True|False) output_directory num_epochs use_grc_lat_dataset(True|False)

as in this example:

    python knowledge_distillation.py bowphs/SPhilberta bowphs/SPhilberta True /directory 1 False

The whiten argument decides if whitening is applied to the teacher embeddings before training.
<br>The use_grc_lat_dataset parameter lets you decide if you want to apply knowledge distillation
with Latin as mediator language (and grc_lat sentences) or with English as mediator language.
However, in both cases, the csv files have to be present in the directory
(grc_lat_dataset.csv for grc_lat; grc_eng_training_big.csv for grc_eng_lat)<br>
To get grc_eng_training_big.csv, execute preprocess_krahne_repo.py in corpus_creation/data_retrieval
with the repository with the parallel sentences downloaded (read README.MD there for further instructions).
Same applies for training.csv (see corpus_creating/data_retrieval).

NOTE:<br>
The file is based on make_multilingual.py, created by Reimers and Gurevych, the authors
of the knowledge distillation paper.

## Post Processing (Whitening/CBIE)

Just call either

    whitening(representations)

or

    cluster_based(representations, n_cluster: int, n_pc: int, hidden_size: int = 768)

with the corresponding parameters.

NOTE:<br>
This file is almost identical with the file Hämmerl et al. used for their paper.