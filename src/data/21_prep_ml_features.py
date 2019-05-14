import logging
import os
import sys

import numpy as np
import pandas as pd

import deeplib as lib

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

base_path = os.path.dirname(sys.argv[0])
data_path = os.path.abspath(os.path.join(base_path, "..", "..", "data"))
embeddings_file = os.path.join(data_path, "tmp", "w2v_320d")
embeddings_matrix_file = os.path.join(data_path, "tmp", "embeddings_matrix.npy")

if not os.path.exists(embeddings_matrix_file):
    logging.info("Tokenizing texts to find vocabulary")
    d = pd.read_csv(os.path.join(data_path, "intermediate", "sentences_ml.csv"))
    _data, vocabulary = lib.tokenize(d.lemmata)
    logging.info("Reading embeddings from {}".format(embeddings_file))
    m = lib.embeddings_matrix(vocabulary, embeddings_file)
    logging.info("Saving embeddings to {}".format(embeddings_matrix_file))
    np.save(embeddings_matrix_file, m)
else:
    logging.info("Embeddings matrix {} already exists, skipping".format(embeddings_matrix_file))
