# Ancient Greek - Latin Semantic Similarity Detection

* This project includes the files used for executing the experiments of this thesis.
* For explanations on how to use the files, look into the relevant subdirectories.


* corpus_creation covers the creation of the evaluation corpus. It relies on data (parallel and monolingual)
* data includes the result of corpus_creation, namely the created corpus data
* evaluation_pipeline is used to calculate embeddings for specific models and evaluate their performance
* cbie_whitening is used to apply whitening or cbie to the computed embeddings, as well as analyze anisotropy
* result_analysis is irrelevant for the thesis; it compares the results of different models
* training is used to train models using different methods (parallel sentences or knowledge distillation)