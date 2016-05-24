import numpy as np
import sys
import pickle

from read_snli_data import *
from constants import *
from neural_net_helpers import *

train_tuples = read_pickle_file(TRAIN_PICKLE_FILE)
dev_tuples = read_pickle_file(DEV_PICKLE_FILE)
X_train, Y_train = zip(*train_tuples)
X_dev, Y_dev = zip(*dev_tuples)
num_train = len(X_train)

# Loads Glove vectors into a dict that maps words to np.arrays
words_to_vecs = loadGloveVectors(GLOVE_DIM)
# For unseen words, create random vectors by augmenting words_to_vecs
addUnseenWords(words_to_vecs, GLOVE_DIM, X_train)

# Map every word in the vocab to an index 
words_to_indices = buildDictionary(words_to_vecs)

f = open('wordsToInd.p', 'wb')
pickle.dump(words_to_indices, f)
f.close()

# Convert the input sentences to lists of lists of indices
Y_seq, Y_words_to_inds, Y_inds_to_words, output_vocab_len = convertYsToIndexSequence(Y_train + Y_dev)

g = open('Y_inds_to_words.p', 'wb')
pickle.dump(Y_inds_to_words, g)
g.close()