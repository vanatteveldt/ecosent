#! /usr/bin/env python3
#DESCRIPTION: Test the learning curve of the chosen CNN model
#DEPENDS: data/intermediate/sentences_ml.csv, data/tmp/w2v_320d
#CREATES: data/intermediate/cnn_curve.csv

import csv
import logging
import random
from pathlib import Path

import numpy as np
import deeplib as lib
from keras import backend as keras_backend

lib.cudnn_error_workaround()

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
output_file = data_root/"intermediate"/"cnn_curve.csv"

logging.info("Loading data")

train_texts, train_labels = lib.get_data(data_file, gold=0)
test_texts, test_labels = lib.get_data(data_file, gold=1)

train_labels = lib.encode_labels(train_labels, output_dim=settings['output_dim'])
test_labels = lib.encode_labels(test_labels, output_dim=settings['output_dim'])

# Tokenize on test data as well because the word_index is also used to initialize the embeddings
# (and since actual words are never used this is permitted, alternative would be to rewrite the tokenization
#  to use vocabulary from embeddings instead, but has the same result for more work)
data, word_index = lib.tokenize(train_texts.append(test_texts))

train_data = data[:len(train_texts)]
test_data = data[len(train_texts):]

logging.info("Loading embeddings")
embeddings = lib.embeddings_matrix(word_index, str(embeddings_file))


with output_file.open('w') as of:
    w = csv.writer(of)
    w.writerow(['i', 'perc', 'n', 'acc', 'cor', 'alpha'])
    of.flush()
    for i in range(50):
        for perc in np.linspace(0.1, 1, 20):
            inc = np.random.choice([True, False], size=len(train_labels), replace=True, p=[perc, 1-perc])
            x = train_data[inc]
            y = train_labels[inc]
            logging.info("Training model on {:.0%} of data: {}".format(perc, x.shape))

            model = lib.cnn_model(settings=settings,
                                  max_sequence_length=train_data.shape[1],
                                  embeddings_matrix=embeddings)

            model.fit(x, y, epochs=settings['epochs'], batch_size=settings['batch_size'], verbose=0)

            output = model.predict(test_data)
            keras_backend.clear_session()

            acc, cor, alpha = lib.validate(output, test_labels)
            w.writerow([i, perc, len(y), acc, cor, alpha])
            of.flush()

