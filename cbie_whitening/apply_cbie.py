# Applies CBIE or Whitening to given embedding vectors and stores it in given output_file
# Call structure: python apply_cbie.py --(whitening|cbie) --input_file xxx.vec --output_file xxx.vec

from gensim.models import KeyedVectors
from post_processing import cluster_based, whitening
from pca_analysis import get_embeddings_as_array
import numpy as np
import sys

cl_args=sys.argv
if not sys.argv[1] in ['--whitening', '--cbie']:
    print("Could not read cmdline arguments")
    exit(1)
whit = False
if sys.argv[1]=='--whitening':
    whit = True
input_file=sys.argv[3]
output_file=sys.argv[5]

embs=KeyedVectors.load_word2vec_format(input_file, binary=False)
embs_arr=get_embeddings_as_array(embs)

print(embs_arr.shape)
if not whit:
    embs_arr = cluster_based(embs_arr, n_cluster=7, n_pc=12, hidden_size=embs_arr.shape[1])
else:
    embs_arr=whitening(embs_arr)
new_embs = KeyedVectors(vector_size=embs_arr.shape[1])
new_embs.add_vectors(embs.index_to_key, embs_arr)
new_embs.save_word2vec_format(output_file, binary=False)
