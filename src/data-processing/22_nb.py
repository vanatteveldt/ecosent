#! /usr/bin/env python3
#DESCRIPTION: Run SVM on the prepared sentences
#DEPENDS: data/intermediate/sentences_ml.csv
#CREATES: data/intermediate/nb_predictions.csv, data/intermediate/nb_features.csv
import logging
import csv
import numpy as np
import pandas as pd
import random
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

random_seed = 1
np.random.seed(random_seed)
random.seed(random_seed)

data_root = Path.cwd()/"data"
data_file = data_root/"intermediate"/"sentences_ml.csv"
output_file = data_root/"intermediate"/"nb_predictions.csv"

feature_file = data_root/"intermediate"/"nb_features.csv"

pipe = Pipeline([("Vectorizer", TfidfVectorizer(min_df=10)),
                 ("scaler", Normalizer()),
                 ("NB", MultinomialNB())])

logging.info("Reading data")
h = pd.read_csv(data_file)

train = h.loc[h['gold'] == 0]
test = h.loc[h['gold'] == 1]

logging.info(f"Fitting model")
train = train.sample(frac=1).reset_index(drop=True)

pipe.fit(train.lemmata.values, train.value.values)
predictions = pipe.predict(test.lemmata.values)
scores = pipe.predict_proba(test.lemmata.values)
acc = sum([a==b for (a,b) in zip(predictions, test.value.values)]) / len(predictions)
logging.info(f"Accuracy on test set: {acc:.4}")

    
with output_file.open('w') as outf:
    w = csv.writer(outf)
    w.writerow(['id', 'confidence', 'value'])
    
    for id, pred, score in zip(test.id.values, predictions, scores):
        score = sorted(score, reverse=True)
        confidence = score[0] - score[1]
        w.writerow([id, confidence, pred])


with feature_file.open('w') as featf:
    w = csv.writer(featf)
    classes = [str(x) for x in pipe['NB'].classes_]
    weights = pipe["NB"]._get_coef()
    w.writerow(["feature"] + classes)
    w.writerow(["___INTERCEPT___"] + [str(x) for x in pipe["NB"]._get_intercept()])
    for i, feature in enumerate(pipe["Vectorizer"].get_feature_names()):
        w.writerow([feature] + [weights[j][i] for j, _ in enumerate(classes)]) 

            
