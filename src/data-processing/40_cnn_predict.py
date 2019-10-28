#! /usr/bin/env python3
#DESCRIPTION: Get final predictions for the best CNN model
#DEPENDS: data/intermediate/sentences_ml.csv, data/tmp/w2v_320d
#CREATES: data/intermediate/cnn_predictions.csv

import csv
import logging
import random
from pathlib import Path

import numpy as np
import pandas as pd
import deeplib as lib
from keras import backend as keras_backend

# best settings according to grid search:
settings = dict(
    train_embedding=True,
    n_hidden=1,
    depth_hidden=64,
    learning_rate=.004,
    epochs=4,
    loss='mean_absolute_error',
    output_dim=2,
    batch_size=128,
    )

random_seed = 1
np.random.seed(random_seed)
random.seed(random_seed)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

data_root = Path.cwd()/"data"
data_file = data_root/"intermediate"/"sentences_ml.csv"
embeddings_file = data_root/"tmp"/"w2v_320d"
output_file = data_root/"intermediate"/"cnn_predictions.csv"

logging.info("Loading data")

data = pd.read_csv(data_file)
# drop gold, randomize rows, select train/val

labels = lib.encode_labels(data.tone, output_dim=settings['output_dim'])

# Tokenize on test data as well because the word_index is also used to initialize the embeddings
# (and since actual words are never used this is permitted, alternative would be to rewrite the tokenization
#  to use vocabulary from embeddings instead, but has the same result for more work)
tokens, word_index = lib.tokenize(data.lemmata)

train_data = tokens[data.gold == 0]
test_data = tokens[data.gold == 1]

train_labels = labels[data.gold == 0]
test_labels = labels[data.gold == 1]

test_ids = data.id[data.gold == 1].values

logging.info("Loading embeddings")
embeddings = lib.embeddings_matrix(word_index, str(embeddings_file))


logging.info(f"Training model on training data {train_data.shape}")

model = lib.cnn_model(settings=settings,
                      max_sequence_length=train_data.shape[1],
                      embeddings_matrix=embeddings)

model.fit(train_data, train_labels, epochs=settings['epochs'], batch_size=settings['batch_size'], verbose=0)

output = model.predict(test_data)
keras_backend.clear_session()

p = list(lib.predict(output))

# Also 'predict' the true labels to convert from N neurons to single value
actual = lib.predict(test_labels)
acc = sum([x == y for (x, y) in zip(p, actual)]) / len(p)
logging.info(f"Accuracy: {acc}")

with output_file.open('w') as outf:
    w = csv.writer(outf)
    w.writerow(["id", "prediction", "actual"])
    for i, pred in enumerate(p):
        w.writerow([test_ids[i], pred, actual[i]])

