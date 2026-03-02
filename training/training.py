import csv
import subprocess
from sentence_transformers import SentenceTransformer, InputExample, losses, models, \
    SentenceTransformerTrainingArguments, SentenceTransformerTrainer
from datasets import Dataset, load_dataset
import os
import json
import torch

model = SentenceTransformer("bowphs/SPhilBerta", device="cuda")

# 1. Define the Transformer (Word Embeddings)
# word_embedding_model = models.Transformer("UGARIT/grc-alignment", max_seq_length=450, config_args={"output_hidden_states": True})
#
# # 2. Add a Custom layer to select the hidden state we want
# class LayerSelector(torch.nn.Module):
#     def __init__(self, layer_idx):
#         super().__init__()
#         self.layer_idx = layer_idx
#
#     def forward(self, features):
#         # features['all_hidden_states'] is a tuple of (batch, seq, hidden_dim)
#         features.update({'token_embeddings': features['all_layer_embeddings'][self.layer_idx]})
#         return features
#
#     def save(self, save_path):
#         """
#         This method is called by SentenceTransformer when saving the model.
#         We save the layer_idx so the model knows which layer to pick when reloaded.
#         """
#         os.makedirs(save_path, exist_ok=True)
#         with open(os.path.join(save_path, 'config_layer.json'), 'w') as fOut:
#             json.dump({'layer_idx': self.layer_idx}, fOut, indent=4)
#
#     @staticmethod
#     def load(input_path):
#         """
#         This method is called by SentenceTransformer when loading the model.
#         """
#         with open(os.path.join(input_path, 'config_layer.json')) as fIn:
#             config = json.load(fIn)
#         return LayerSelector(**config)
#
# # 3. Define the Pooling layer (Sentence Embeddings)
# pooling_model = models.Pooling(
#     word_embedding_model.get_word_embedding_dimension(),
#     pooling_mode_mean_tokens=True
# )
# # 4. Assemble: Transformer -> LayerSelector -> Pooling
# layer_idx = 8
# model = SentenceTransformer(modules=[
#     word_embedding_model,
#     LayerSelector(layer_idx),
#     pooling_model
# ])

train_dataset = load_dataset("csv", data_files="training.csv")
cols = train_dataset["train"].column_names
train_loss = losses.CachedMultipleNegativesRankingLoss(model, mini_batch_size=64)

args = SentenceTransformerTrainingArguments(
    output_dir='sphilberta_unpr_big',
    num_train_epochs=8,
    per_device_train_batch_size=256,
    per_device_eval_batch_size=256,
    save_strategy="epoch",
    logging_strategy="steps",
    logging_steps=10,
    logging_dir="logs",
    logging_first_step=True,
    save_total_limit=4,
    dataloader_num_workers=0,
    remove_unused_columns=False,
    report_to='none'
)
# optimizer steps per epoch = ceil(num_examples / (accum_steps))
import math
steps_per_epoch = math.ceil(10000 / (256))
total_optimizer_steps = steps_per_epoch * 8
warmup_steps = max(1, int(0.1 * total_optimizer_steps))
args.warmup_steps=warmup_steps
# Train
trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    loss=train_loss
)

trainer.train()

trainer.save_model("sphilberta_unpr_big")
