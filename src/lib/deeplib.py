import csv
from typing import Tuple, Sequence

import krippendorff
import numpy as np
import pandas as pd
from keras.callbacks import Callback
from keras.layers import Dense, Input, GlobalMaxPooling1D, Conv1D, Embedding
from keras.models import Model
from keras.optimizers import RMSprop
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical

MAX_NB_WORDS=10000

def cudnn_error_workaround():
    """
    Workaround for CUDNN_STATUS_INTERNAL_ERROR
    See https://github.com/tensorflow/tensorflow/issues/24496
    """
    from tensorflow.compat.v1 import ConfigProto
    from tensorflow.compat.v1 import InteractiveSession
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    InteractiveSession(config=config)



def embeddings_matrix(vocabulary, embeddings_file):
    """Load the embeddings and create a initial weights matrix

    @param vocabulary: Mapping of word to index (i.e. the Tokenizer word_index)
    """
    import gensim
    embeddings = gensim.models.Word2Vec.load(embeddings_file)
    embedding_matrix = np.zeros((len(vocabulary) + 1, embeddings.vector_size))
    for word, i in vocabulary.items():
        if word in embeddings.wv:
            embedding_matrix[i] = embeddings.wv[word]
    return embedding_matrix


def get_data(data_file, shuffle=True, gold=0):
    """Get the data, returning the texts and labels"""
    h = pd.read_csv(data_file)
    # drop gold, randomize rows, select train/val
    h = h[h.gold == gold]
    if shuffle:
        h = h.sample(frac=1).reset_index(drop=True)
    texts = h.lemmata
    labels = h.tone
    return texts, labels


def encode_labels(labels: Sequence[int], output_dim: int) -> np.array:
    if output_dim == 1:
        return np.asarray([[x] for x in labels])
    elif output_dim == 2:
        return np.asarray([[(x + 1) / 2, int(x != 0)] for x in labels])
    elif output_dim == 3:
        labels = [tone+1 for tone in labels] # -1 -> 0 etc
        return to_categorical(np.asarray(labels))
    else:
        raise ValueError(output_dim)


def tokenize(texts):
    """Tokenize the sentences, returning the dtm and vocabulary"""
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(texts)
    word_index = tokenizer.word_index
    sequences = tokenizer.texts_to_sequences(texts)
    data = pad_sequences(sequences)
    return data, word_index


def get_final_activation(output_dim):
    if output_dim == 1:
        return 'tanh' # -1 .. 1
    if output_dim == 2:
        return 'sigmoid'  # 2x 0..1
    if output_dim == 3:
        return 'softmax' # 3x 0..1 summing to 1


def cnn_model(settings, max_sequence_length, embeddings_matrix):
    embedding_layer = Embedding(embeddings_matrix.shape[0],
                                embeddings_matrix.shape[1],
                                weights=[embeddings_matrix],
                                input_length=max_sequence_length,
                                trainable=settings['train_embedding'])
    
    sequence_input = Input(shape=(max_sequence_length,), dtype='int32')
    embedded_sequences = embedding_layer(sequence_input)
    
    x = Conv1D(128, 3, activation='relu')(embedded_sequences)
    x = GlobalMaxPooling1D()(x)
    for i in range(settings['n_hidden']):
        x = Dense(settings['depth_hidden'], activation='relu')(x)
    preds = Dense(settings['output_dim'], activation=get_final_activation(settings['output_dim']))(x)
    model = Model(sequence_input, preds)
    optimizer = RMSprop(lr=settings['learning_rate'])
    loss = settings['loss']
    #if loss == 'dynamic':
    #    loss = 'binary_crossentropy' if settings['output_dim'] == 3 else 'mean_absolute_error'

    model.compile(loss=loss, optimizer=optimizer)
    return model


class ValidationLogger(Callback):
    def __init__(self, keys, outfile):
        self.keys = keys
        self.output_file = open(outfile, 'w')
        self.w = csv.writer(self.output_file)
        self.w.writerow(["rep", "experiment"] + keys + ["epoch", "fold", "acc", "cor", "mse", "cortot"])
        self.experiment = 0

    def start_experiment(self, settings, rep=None, i=None):
        self.fold = 0
        self.rep = rep
        if i is None:
            self.experiment += 1
        else:
            self.experiment = i
        self.settings_row = [self.rep, self.experiment] + [settings[k] for k in self.keys]

    def start_fold(self, x_val, y_val):
        self.fold += 1
        self.x_val = x_val
        self.y_val = y_val

    def get_prediction(self):
        predictions = self.model.predict(self.x_val)
        
    def on_epoch_end(self, epoch, logs):
        output = self.model.predict(self.x_val)
        acc, cor, alpha = validate(output, self.y_val)

        mse = 0; cortot = 0; dim = output.shape[1]
        for i in range(dim):
            preds = [p[i] for p in output]
            act = [p[i] for p in self.y_val]
            
            mse += sum([(x - y)**2 for (x, y) in zip(preds, act)]) / len(preds)
            cortot += np.corrcoef(preds, act)[1][0]
        mse = mse / dim
        cortot = cortot / dim
                
        self.w.writerow(self.settings_row + [epoch, self.fold, acc, cor, mse, cortot])
        self.output_file.flush()


def validate(output, test_labels) -> Tuple[float, float, float]:
    p = list(predict(output))
    # Also 'predict' the true labels to convert from N neurons to single value
    actual = predict(test_labels)
    acc = sum([x == y for (x, y) in zip(p, actual)]) / len(p)
    cor = np.corrcoef(p, actual)[1][0]
    alpha = krippendorff.alpha(np.vstack([p, actual]), level_of_measurement='interval')
    return acc, cor, alpha


def xval_folds(x, y, folds=5):
    nval = len(y) // folds
    splits = np.array([nval * (f+1) for f in range(folds)])
    y_folds = np.split(y, splits)
    x_folds = np.vsplit(x, splits)
    for i in range(folds):
        x_train = np.vstack([x_folds[j] for j in range(folds) if j != i])
        y_train = np.concatenate([y_folds[j] for j in range(folds) if j != i])
        x_val = x_folds[i]
        y_val = y_folds[i]
        yield x_train, y_train, x_val, y_val


def predict(output):
    """Convert NN output to {-1, 0, 1}"""
    dim = output.shape[1]
    if dim == 1:
        return [x[0] > .33 and 1 or (x[0] < -.33 and -1 or 0) for x in output]
    if dim == 2:
        return [0 if x[1] < .5 else (x[0] < 0.5 and -1 or 1) for x in output]
    if dim == 3:
        return list(np.argmax(output, axis=1) - 1)


def iter_grid(grid):
    """
    Iterate over all options (combinations) in the grid.
    
    @param grid: list of (name, list-of-options) pairs
    @return: a generator of dict {name: option}
    """
    if isinstance(grid, dict):
        grid = sorted(grid.items())
    (name, options), tail = grid[0], grid[1:]
    for option in options:
        tail_options = iter_grid(tail) if tail else [{}]
        for tail_option in tail_options:
            yield {name: option, **tail_option}


if __name__ == '__main__':
    t, l = get_data("../sentences_ml2.csv", 1, shuffle=False)
    print(l)
    print(np.asarray(predict(l)))
    print("### 2")
    t, l = get_data("../sentences_ml2.csv", 2, shuffle=False)
    print(l)
    print(np.asarray(predict(l)))
    print("### 3")
    t, l = get_data("../sentences_ml2.csv", 3, shuffle=False)
    print(l)
    print(np.asarray(predict(l)))
