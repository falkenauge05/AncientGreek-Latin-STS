# Calculates isotropy and outlier dimensions of embeddings (source of embeddings is to be adjusted below)

import numpy as np
from gensim.models import KeyedVectors

def get_embeddings_as_array(w2v):
    res = np.ones((len(w2v.key_to_index), w2v.vector_size)).astype('float32')

    for i, w in enumerate(w2v.key_to_index):
        res[i] = w2v[w]/np.linalg.norm(w2v[w])

    return res

#adjust input files here
se = KeyedVectors.load_word2vec_format("grc-lat.test.grc.vec", binary=0, encoding='utf-8', unicode_errors='replace', limit=None)
te = KeyedVectors.load_word2vec_format("grc-lat.test.lat.vec", binary=0, encoding='utf-8', unicode_errors='replace', limit=None)

se_array = get_embeddings_as_array(se)
te_array = get_embeddings_as_array(te)

print("BEGIN CALCULATING")
# Now isotropy is calculated (mean cosine similarity over all embeddings)

# Cosine similarity matrix (N x N), since embeddings already got normalized (get_embeddings_as_array), only dot product necessary
# -> matrix multiplication
cos_sim_matrix = se_array @ te_array.T

avg_sim=np.sum(cos_sim_matrix)/(se_array.shape[0]*te_array.shape[0])

print("Average cosine similarity (overall):", avg_sim)

# Mean of each dimension
X_mean = np.mean(se_array, axis=0)  # (D,)
Y_mean = np.mean(te_array, axis=0)  # (D,)

# Average cosine contribution per dimension
avg_cosine_per_dim = X_mean * Y_mean

mu=np.mean(avg_cosine_per_dim)
sigma=np.std(avg_cosine_per_dim)
z_scores=(avg_cosine_per_dim-mu)/sigma
outlier_mask=np.abs(z_scores)>5
outlier_dims=np.where(outlier_mask)[0]
print(outlier_dims)

# give the dimensions numbers
avg_cosine_per_dim_with_number=[]
for i, avg_cos in enumerate(avg_cosine_per_dim):
    avg_cosine_per_dim_with_number.append((i, avg_cos))

# sort by highest anisotropy
avg_cosine_per_dim_with_number.sort(key=lambda x: x[1], reverse=True)

# print 10 dimensions with highest anisotropy together with anisotropy value
print("Average cosine similarity per dimension:")
print(avg_cosine_per_dim_with_number[:10])
