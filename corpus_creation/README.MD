# Corpus Creation

* prepare_monolingual_dataset.py and prepare_parallel_dataset.py are internal files you can call if you have your parallel data in the same format
  (multiple text files aligned with .gre.txt and .lat.txt file endings and same numeration for parallel files; txt files in one directory (one sentence per line) in the monolingual case)
* preprocess_corpus_data.py removes any Greek alphabet Latin sentences, replaces j by i, removes excessive whitespaces
* Alter the paths in the last blocks of corpus_creation.py to your monolingual and parallel sentence files, then execute it
to create the corpus with your specified data.

NOTE: the files are taken from Okabe et Fraser (2025), bilingual sentence mining for low resource languages