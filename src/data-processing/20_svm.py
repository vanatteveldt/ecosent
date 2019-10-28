#! /usr/bin/env python3
#DESCRIPTION: Run SVM on the prepared sentences
#DEPENDS: data/intermediate/sentences_ml.csv
#CREATES: data/intermediate/svm_predictions.csv

import logging
import csv
import numpy as np
import pandas as pd
import random
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

random_seed = 1
np.random.seed(random_seed)
random.seed(random_seed)

data_root = Path.cwd()/"data"
data_file = data_root/"intermediate"/"sentences_ml.csv"
output_file = data_root/"intermediate"/"svm_predictions.csv"

C = 1
gamma = .1
kernel = 'linear'

pipe = Pipeline([("Vectorizer", TfidfVectorizer(min_df=10)),
                 ("scaler", Normalizer()),
                 ("SVC", SVC(C=C, gamma=gamma, kernel=kernel))])

logging.info("Reading data")
h = pd.read_csv(data_file)

train = h.loc[h['gold'] == 0]
test = h.loc[h['gold'] == 1]

logging.info("Fitting model")
pipe.fit(train.lemmata.values, train.tone.values)
logging.info("Predicting gold data")
predictions = pipe.predict(test.lemmata.values)

acc = sum([a==b for (a,b) in zip(predictions, test.tone.values)]) / len(predictions)
logging.info("Accuracy on test set: {:.3}".format(acc))
with output_file.open('w') as outf:
    w = csv.writer(outf)
    w.writerow(['kernel', 'gamma', 'C', 'id', 'prediction'])
    for i, pred in enumerate(predictions):
        w.writerow([kernel, gamma, C, test.id.values[i], pred])
