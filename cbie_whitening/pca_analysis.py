import sklearn.decomposition as decomposition
from gensim.models import KeyedVectors
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

def get_embeddings_as_array(w2v):
    res = np.ones((len(w2v.key_to_index), w2v.vector_size)).astype('float32')

    for i, w in enumerate(w2v.key_to_index):
        res[i] = w2v[w]/np.linalg.norm(w2v[w])

    return res
def test():
    antiquity = KeyedVectors.load_word2vec_format("antiquity.vec", encoding='utf-8', unicode_errors='replace')
    antiquity_arr=get_embeddings_as_array(antiquity)
    #renaissance = KeyedVectors.load_word2vec_format("renaissance.vec", encoding='utf-8', unicode_errors='replace')
    #renaissance_arr=get_embeddings_as_array(renaissance)
    #modern = KeyedVectors.load_word2vec_format("modern.vec", encoding='utf-8', unicode_errors='replace')
    #modern_arr=get_embeddings_as_array(modern)
    #anitiquity2=KeyedVectors.load_word2vec_format("new_testament.vec", encoding='utf-8', unicode_errors='replace')
    #antiquity2_arr=get_embeddings_as_array(anitiquity2)
    #antiquity2_arr=antiquity2_arr[:100, :]
    medieval = KeyedVectors.load_word2vec_format("medieval.vec", encoding='utf-8', unicode_errors='replace')
    medieval_arr=get_embeddings_as_array(medieval)
    combined_array=np.concatenate((antiquity_arr, medieval_arr))
    res=decomposition.PCA(n_components=2).fit_transform(combined_array)

    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot(111)

    colors = np.array([0]*len(antiquity_arr)+ ([1]*len(medieval_arr)))

    scatter = ax.scatter(
        res[:, 0],
        res[:, 1],
        c=colors,
        s=40,
    )
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Boethius',
               markerfacecolor=plt.cm.viridis(0), markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Medieval',
               markerfacecolor=plt.cm.viridis(1.0), markersize=8)
        #Line2D([0], [0], marker='o', color='w', label='New Testament',
        #       markerfacecolor=plt.cm.viridis(1/3), markersize=8),
        #Line2D([0], [0], marker='o', color='w', label='Renaissance',
        #       markerfacecolor=plt.cm.viridis(2/3), markersize=8),
        #Line2D([0], [0], marker='o', color='w', label='Modern',
        #        markerfacecolor=plt.cm.viridis(3/3), markersize=8)
    ]
    ax.legend(handles=legend_elements, loc="best")
    plt.show()