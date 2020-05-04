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

with output_file.open('w') as outf:
    w = csv.writer(outf)
    w.writerow(['id', 'confidence', 'value'])
    logging.info(f"Fitting model")
    train = train.sample(frac=1).reset_index(drop=True)

    pipe.fit(train.lemmata.values, train.value.values)
    predictions = pipe.predict(test.lemmata.values)
    scores = pipe.decision_function(test.lemmata.values)
    
    acc = sum([a==b for (a,b) in zip(predictions, test.value.values)]) / len(predictions)
    logging.info(f"Accuracy on test set: {acc:.4}")
    
    for id, pred, score in zip(test.id.values, predictions, scores):
        score = sorted(score, reverse=True)
        confidence = score[0] - score[1]
        w.writerow([id, confidence, pred])

