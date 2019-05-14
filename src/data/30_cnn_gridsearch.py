# Run a grid search of the CNN model
# Requires:
#  - the initialized embeddings matrix (tmp/embeddings.npy) created by prep_ml_features.py
#  - the lemmata and codings (intermediate/sentences_ml.csv) created by ml_features.R

import sys
import os
import logging

import deeplib as lib
import numpy as np
from keras import backend as keras_backend

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

FN_DATA = "sentences_ml2.csv"
FN_EMBEDDINGS = 'embeddings.npy'
OUTFILE = sys.argv[1]

N_EPOCHS = 10
BATCH_SIZE = 128

PARAM_GRID = dict(
    train_embedding = [True],
    n_hidden = [1],
    depth_hidden = [32, 64, 96, 128],
    learning_rate = [.01, .004, 0.002, 0.001, .0005, .0001],
    loss = ['mean_absolute_error', 'binary_crossentropy', 'mean_squared_error'],
    output_dim = [1,2,3]
    )

logging.info("Loading data from {} and {}, saving logs to {}".format(FN_DATA, FN_EMBEDDINGS, OUTFILE))
embeddings = np.load(FN_EMBEDDINGS)

params = sorted(PARAM_GRID)

logger = lib.ValidationLogger(params, OUTFILE)

experiments = list(lib.iter_grid(PARAM_GRID))

for i, settings in enumerate(experiments):
    logging.info("Experiment {i}/{n}: {settings}".format(n=len(experiments), **locals()))
    logger.start_experiment(settings)
    texts, labels = lib.get_data(FN_DATA, output_dim=settings['output_dim'])
    data, word_index = lib.tokenize(texts)

    for j, (x_train, y_train, x_val, y_val) in enumerate(lib.xval_folds(data, labels)):
        logging.info("... Fold {}. #train: {}, #val: {}".format(j, len(y_train), len(y_val)))
        logger.start_fold(x_val, y_val)
        model = lib.cnn_model(settings=settings,
                              max_sequence_length=data.shape[1],
                              embeddings_matrix=embeddings)

        model.fit(x_train, y_train, epochs=N_EPOCHS, batch_size=BATCH_SIZE, callbacks=[logger])
        keras_backend.clear_session()

