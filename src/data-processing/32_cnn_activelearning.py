"""
Tests the learning curve of the chosen CNN model
Requires:
  - the initialized embeddings matrix (tmp/embeddings.npy) created by prep_ml_features.py
  - the lemmata and codings (intermediate/sentences_ml.csv) created by ml_features.R

From the grid search, use: output_dim=1, 64 hidden neurons, MAE loss function, .004 learning rate, 4 epochs

"""
import csv
import logging
import os
import sys
import numpy as np
import deeplib as lib
import krippendorff
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

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

base_path = os.path.dirname(sys.argv[0])
data_path = os.path.abspath(os.path.join(base_path, "..", "..", "data"))
data_file = os.path.join(data_path, "intermediate", "sentences_ml.csv")
output_file = os.path.join(data_path, "intermediate", "activelearning_dim2.csv")
embeddings_file = os.path.join(data_path, "tmp", "w2v_320d")

logging.info("Loading data")

train_texts, train_labels = lib.get_data(data_file, output_dim=settings['output_dim'], gold=0)
test_texts, test_labels = lib.get_data(data_file, output_dim=settings['output_dim'], gold=1)

# we tokenize on test data as well because the word_index is also used to initialize the embeddings
data, word_index = lib.tokenize(train_texts.append(test_texts))

train_data = data[:len(train_texts)]
test_data = data[len(train_texts):]

logging.info("Loading embeddings")
embeddings = lib.embeddings_matrix(word_index, embeddings_file)
#embeddings = np.load(os.path.join(data_path, "tmp", "embeddings_matrix.npy"))


np.random.seed(1)
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

