#! /usr/bin/env python3
#DESCRIPTION: Run a grid search to find optimal CNN parameters
#DEPENDS: data/intermediate/sentences_ml.csv, data/tmp/w2v_320d
#CREATES: data/intermediate/gridsearch.csv

# Run a grid search of the CNN model
# Requires:
#  - the initialized embeddings matrix (tmp/embeddings.npy) created by prep_ml_features.py
#  - the lemmata and codings (intermediate/sentences_ml.csv) created by ml_features.R
import random
import sys
import logging

import os
from pathlib import Path

import deeplib as lib
import numpy as np
from keras import backend as keras_backend

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

random_seed = 1
np.random.seed(random_seed)
random.seed(random_seed)

data_root = Path.cwd()/"data"
data_file = data_root/"intermediate"/"sentences_ml.csv"
output_file = data_root/"intermediate"/"gridsearch.csv"
embeddings_file = data_root/"tmp"/"w2v_320d"

N_EPOCHS = 10
BATCH_SIZE = 128
N_FOLDS = 10
N_REPEAT = 4

PARAM_GRID = dict(
    train_embedding=[True, False],
    n_hidden=[0, 1, 2],
    depth_hidden=[32, 64, 96, 128],
    learning_rate=[.01, .004, 0.002, 0.001, .0005, .0001],
    loss=['mean_absolute_error', 'binary_crossentropy', 'mean_squared_error'],
    output_dim=[1, 2, 3]
    )

logging.info(f"Loading data from {data_file} and {embeddings_file}, saving logs to {output_file} (seed={random_seed})")
texts, labels = lib.get_data(data_file, shuffle=True)
data, vocabulary = lib.tokenize(texts)

logging.info("Loading embeddings")
embeddings = lib.embeddings_matrix(vocabulary, str(embeddings_file))

params = sorted(PARAM_GRID)
logger = lib.ValidationLogger(params, output_file)

experiments = list(lib.iter_grid(PARAM_GRID))

for rep in range(N_REPEAT):
    for i, settings in enumerate(experiments):
        logging.info(f"Rep {rep}/{N_REPEAT}, experiment {i}/{len(experiments)}: {settings}")
        logger.start_experiment(settings, rep=rep)

        labels_enc = lib.encode_labels(labels, output_dim=settings['output_dim'])
        for j, (x_train, y_train, x_val, y_val) in enumerate(lib.xval_folds(data, labels_enc, folds=N_FOLDS)):
            logging.info("... Fold {}. #train: {}, #val: {}".format(j, len(y_train), len(y_val)))
            logger.start_fold(x_val, y_val)
            model = lib.cnn_model(settings=settings,
                                  max_sequence_length=data.shape[1],
                                  embeddings_matrix=embeddings)

            model.fit(x_train, y_train, epochs=N_EPOCHS, batch_size=BATCH_SIZE, callbacks=[logger])
            keras_backend.clear_session()

