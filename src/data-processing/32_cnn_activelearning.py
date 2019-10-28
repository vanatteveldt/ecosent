#! /usr/bin/env python3
#DESCRIPTION: Test the learning curve of the chosen CNN model
#DEPENDS: data/intermediate/sentences_ml.csv, data/tmp/w2v_320d
#CREATES: data/intermediate/activelearning.csv

import csv
import logging
from pathlib import Path
import random

import numpy as np
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
output_file = data_root/"intermediate"/"activelearning.csv"

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

PER_BATCH = 505

with open(output_file, 'w') as of:
    w = csv.writer(of)
    w.writerow(['i', 'n', 'acc', 'cor', 'alpha'])
    of.flush()
    for i in range(50):
        all_ids = set(range(len(train_labels)))
        train = set(np.random.choice(list(all_ids), size=PER_BATCH, replace=False))
        tail = all_ids - train
        while True:
            logging.info("Training model on {}, #left: {}".format(len(train), len(tail)))
            ids = sorted(train)
            x = train_data[ids]
            y = train_labels[ids]
            keras_backend.clear_session()
            model = lib.cnn_model(settings=settings,
                                  max_sequence_length=train_data.shape[1],
                                  embeddings_matrix=embeddings)
            model.fit(x, y, epochs=settings['epochs'], batch_size=settings['batch_size'], verbose=0)

            logging.info("Logging performance on gold set")
            output = model.predict(test_data)
            acc, cor, alpha = lib.validate(output, test_labels)
            w.writerow([i, len(y), acc, cor, alpha])
            of.flush()

            if not tail:
                logging.info("Done!")
                break
            elif len(tail) < PER_BATCH:
                logging.info("Adding last batch of {} to training".format(len(tail)))
                train |= tail
                tail = set()
            else:
                logging.info("Predicting remaining articles to select for training")
                candidates = np.array(sorted(tail))
                predictions = model.predict(train_data[candidates])
                if settings['output_dim'] == 1:
                    # sentiment from -1..1 -> confidence is how far is the number from +/- 0.5 ?
                    predictions = predictions[:, 0]
                    confidence = np.abs(np.abs(predictions) - .5)
                elif settings['output_dim'] == 2:
                    # has_sentiment, sentiment both 0..1 -> confidence is sum of how far either number is from 0.5
                    confidence = np.abs(predictions - 0.5)
                    confidence = confidence[:, 0] + confidence[:, 1]
                else:
                    raise Exception("Not implemented")
                select = np.argsort(confidence)[:PER_BATCH]
                select_ids = set(candidates[select])
                train |= select_ids
                tail -= select_ids

