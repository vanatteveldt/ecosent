# Economic Sentiment
Data &amp; Analysis compendium for the Economic Sentiment analysis paper.

# Article

View the [preprint of the article here](report/atteveldt_sentiment.pdf).

# Code

The main analysis code is located in the [src/data-processing](src/data-processing). 
Of interest might be:

* [10_apply_dictionaries.py](src/data-processing/) Sentiment Dictionaries (Python)
* [11_apply_dictionaries_quanteda.R](src/data-processing/11_apply_dictionaries_quanteda.R) Sentiment Dictionaries (Quanteda)
* [20_svm.py](src/data-processing/20_svm.py) Support Vector Machines
* [22_nb.py](src/data-processing/22_nb.py) Naive Bayes
* [40_cnn_predict.py](src/data-processing/40_cnn_predict.py) Convolutional Neural Network

# Data

The following data files might be of interest:

* [metadata.csv](data/intermediate/metadata.csv) Headline, date, and source of each article
* [gold.csv](data/intermediate/gold.csv) Gold standard (expert) coding
* [crowdcodings.csv](data/intermediate/crowdcodings.csv) Crowd codings 
* [manual_coding.csv](data/intermediate/manual_coding.csv) Manual (student) coding of headlines

See the files in [src/data](src/data) for details on how these files were constructed.

# Results as presented in the article

* [Performance, learning curve, correlations](src/analysis/performance.md)

# Supplementary Results

* [Confusion Matrices of all methods](src/analysis/confusion_matrix.md)
* [Grid Search for CNN](src/analysis/cnn_gridsearch.md) (code: [30_cnn_gridsearch.py](src/data-processing/30_cnn_gridsearch.py)
* [Grid Search for SVM](src/analysis/svm_gridsearch.md) (code: [19_svm_gridsearch.py](src/data-processing/19_svm_gridsearch.py)
* [Validation of ML results against student codings](src/analysis/ml_versus_students.md)
