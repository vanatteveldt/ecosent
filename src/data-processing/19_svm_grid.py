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

from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import deeplib as lib
logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

random_seed = 1
np.random.seed(random_seed)
random.seed(random_seed)

data_root = Path.cwd()/"data"
data_file = data_root/"intermediate"/"sentences_ml.csv"
output_file = data_root/"intermediate"/"svm_grid.csv"

N_REPEAT = 10

PARAM_GRID = dict(
    kernel=['linear', 'poly', 'rbf'],
    C = [10**x for x in np.arange(-3, 3.5, .5)],
    gamma=['scale', 'auto'] + [10**x for x in np.arange(-3, 3.5, .5)]
    )


logging.info("Reading data")
d = pd.read_csv(data_file)
d = d.loc[d['gold'] == 0]

experiments = list(lib.iter_grid(PARAM_GRID))
with output_file.open('w') as outf:
    w = csv.writer(outf)
    w.writerow(['rep', 'experiment', 'kernel', 'C', 'gamma', 'fold', 'f1_macro', 'f1_micro', 'accuracy'])
    for rep in range(N_REPEAT):
        for i, settings in enumerate(experiments):

            logging.info(f"[{rep}/{N_REPEAT}][{i}/{len(experiments)}] Fitting model: {settings}")
            pipe = Pipeline([("Vectorizer", TfidfVectorizer(min_df=10)),
                             ("scaler", Normalizer()),
                             ("SVC", SVC(C=settings['C'], gamma=settings['gamma'], kernel=settings['kernel']))])
            # Shuffle data
            d = d.sample(frac=1).reset_index(drop=True)

            scores = cross_validate(pipe, d.lemmata.values, d.value.values, cv=5, scoring=['f1_macro', 'f1_micro', 'accuracy'])
            for f, (f1_macro, f1_micro, accuracy) in enumerate(zip(scores['test_f1_macro'], scores['test_f1_micro'], scores['test_accuracy'] )):
                w.writerow([rep, i, settings['kernel'], settings['C'], settings['gamma'], f, f1_macro, f1_micro, accuracy])
                outf.flush()

