# Run a grid search of the CNN model
# Requires:
#  - the initialized embeddings matrix (tmp/embeddings.npy) created by prep_ml_features.py
#  - the lemmata and codings (intermediate/sentences_ml.csv) created by ml_features.R
import random
import sys
import logging

import os
import lib.deeplib as lib
import numpy as np
from keras import backend as keras_backend

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

random_seed = int(sys.argv[1])
np.random.seed(random_seed)
random.seed(random_seed)

base_path = os.path.dirname(sys.argv[0])
data_path = os.path.abspath(os.path.join(base_path, "..", "..", "data"))
data_file = os.path.join(data_path, "intermediate", "sentences_ml.csv")
output_file = os.path.join(data_path, "intermediate", "gridsearch_{seed}.csv".format(seed=random_seed))
embeddings_file = os.path.join(data_path, "tmp", "w2v_320d")

N_EPOCHS = 10
BATCH_SIZE = 128
N_FOLDS=10
N_REPEAT=4

PARAM_GRID = dict(
    train_embedding=[True, False],
    n_hidden=[0, 1, 2],
    depth_hidden=[32, 64, 96, 128],
    learning_rate=[.01, .004, 0.002, 0.001, .0005, .0001],
    loss=['mean_absolute_error', 'binary_crossentropy', 'mean_squared_error'],
    output_dim=[1, 2, 3]
    )

logging.info("Loading data from {} and {}, saving logs to {} (seed={})".format(data_file, embeddings_file, output_file, random_seed))
texts, labels = lib.get_data(data_file, shuffle=True)
data, vocabulary = lib.tokenize(texts)

logging.info("Loading embeddings")
embeddings = lib.embeddings_matrix(vocabulary, embeddings_file)

params = sorted(PARAM_GRID)
logger = lib.ValidationLogger(params, output_file)

experiments = list(lib.iter_grid(PARAM_GRID))

for i, settings in enumerate(experiments):
    logging.info("Experiment {i}/{n}: {settings}".format(n=len(experiments), **locals()))
    logger.start_experiment(settings, seed=random_seed)

    labels_enc = lib.encode_labels(labels, output_dim=settings['output_dim'])
    for j, (x_train, y_train, x_val, y_val) in enumerate(lib.xval_folds(data, labels_enc, folds=N_FOLDS)):
        logging.info("... Fold {}. #train: {}, #val: {}".format(j, len(y_train), len(y_val)))
        logger.start_fold(x_val, y_val)
        model = lib.cnn_model(settings=settings,
                              max_sequence_length=data.shape[1],
                              embeddings_matrix=embeddings)

        model.fit(x_train, y_train, epochs=N_EPOCHS, batch_size=BATCH_SIZE, callbacks=[logger])
        keras_backend.clear_session()

