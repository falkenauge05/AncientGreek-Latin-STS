# Data Retrieval

* This is largely for internal purposes (to preprocess source files in xml or other formats to ways usable for us)
* With preprocess_krahne_repo.py, one can convert the data from the Krahne repository
(the Greek-English parallel sentences) into a CSV file given the correct file path
* To generate training.csv with parallel Latin-Greek data, execute the following with the
necessary data in it (this means, DFGH corpus files with correct direcory (change in file) and the thukydides latin and greek xml file from perseus project):


    python preprocess_thukydides.py

    python preprocess_DFGH.py

    python process_training_csv.py

