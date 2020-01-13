#! /usr/bin/env python3
#DESCRIPTION: Run SVM on the prepared sentences
#DEPENDS: data/intermediate/sentences_ml.csv
#CREATES: data/intermediate/svm_curve.csv

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

import deeplib as lib
import krippendorff

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

random_seed = 1
np.random.seed(random_seed)
random.seed(random_seed)

data_root = Path.cwd()/"data"
data_file = data_root/"intermediate"/"sentences_ml.csv"
output_file = data_root/"intermediate"/"svm_curve.csv"

C = 1
gamma = .1
kernel = 'linear'

logging.info("Reading data")
h = pd.read_csv(data_file)

train = h.loc[h['gold'] == 0]
test = h.loc[h['gold'] == 1]

with output_file.open('w') as of:
    w = csv.writer(of)
    w.writerow(['i', 'perc', 'n', 'acc', 'cor', 'alpha'])
    of.flush()
    for i in range(50):
        for perc in np.linspace(0.1, 1, 20):
            inc = np.random.choice([True, False], size=len(train), replace=True, p=[perc, 1-perc])
            x = train[inc]
            logging.info("Training model on {:.0%} of data: {}".format(perc, x.shape))

            pipe = Pipeline([("Vectorizer", TfidfVectorizer(min_df=10)),
                 ("scaler", Normalizer()),
                 ("SVC", SVC(C=C, gamma=gamma, kernel=kernel))])

            pipe.fit(x.lemmata.values, x.tone.values)
            p = pipe.predict(test.lemmata.values)
            actual = test.tone.values
            
            acc = sum([x == y for (x, y) in zip(p, actual)]) / len(p)
            cor = np.corrcoef(p, actual)[1][0]
            alpha = krippendorff.alpha(np.vstack([p, actual]), level_of_measurement='interval')

            w.writerow([i, perc, x.shape[0], acc, cor, alpha])
            logging.info(f"...  acc={acc}")
            of.flush()

