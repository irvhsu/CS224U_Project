# from __future__ import print_function
# from preprocessData import preprocess, convertToOneHot
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, TimeDistributedDense, RepeatVector
from keras.layers.embeddings import Embedding
from keras.layers import recurrent
from read_snli_data import *
from constants import *
from neural_net_helpers import *

def main():
	# Read pickled training and dev files
	train_tuples = read_pickle_file(TRAIN_PICKLE_FILE)
	dev_tuples = read_pickle_file(DEV_PICKLE_FILE)
	X_train, Y_train = zip(*train_tuples)
	X_dev, Y_dev = zip(*dev_tuples)

	num_train = len(X_train)

	# Loads Glove vectors into a dict that maps words to np.arrays
	words_to_vecs = loadGloveVectors(GLOVE_DIM)
	# For unseen words, create random vectors by augmenting words_to_vecs
	addUnseenWords(words_to_vecs, GLOVE_DIM, X_train + X_dev + Y_train + Y_dev)

	print('Words_to_vecs length:', len(words_to_vecs))
	print 'Vector for hi:', words_to_vecs['hi']

	# Map every word in the vocab to an index 
	words_to_indices = buildDictionary(words_to_vecs)
	print 'Words_to_indices length:', len(words_to_vecs)
	print 'Index for hi:', words_to_indices['hi']

	# Get final embedding matrix
	embedding_matrix = createEmbeddingMatrix(words_to_vecs, words_to_indices)
	print 'Embedding Matrix Shape:', embedding_matrix.shape

	print("Converting input sequences to lists of indices...")
	# Convert the input sentences to lists of lists of indices
	X_train_feats = convertToIndexSequence(X_train, words_to_indices)
	X_dev_feats = convertToIndexSequence(X_dev, words_to_indices)
	Y_train_feats = convertToIndexSequence(Y_train, words_to_indices)
	Y_dev_feats = convertToIndexSequence(Y_dev, words_to_indices)

	print("Padding sequences to the same length...")
	X_feats = sequence.pad_sequences(X_train_feats+X_dev_feats, padding='pre')
	X_train_feats = X_feats[:num_train]
	X_dev_feats = X_feats[num_train:]
	Y_feats = sequence.pad_sequences(Y_train_feats+Y_dev_feats, padding='post')

	print 'X Train Feats Shape:', X_train_feats.shape
	print 'X Train Feats[0]:', X_train_feats[0]

	print("Converting output sentences to one-hot...")
	# Y_feats = convertToOneHot(Y_feats, len(embedding_matrix))
	# Y_train_feats = Y_feats[:num_train]
	# Y_dev_feats = Y_feats[num_train:]

	# print 'Y Train Feats Shape:', Y_train_feats.shape
	# print 'Y Train Feats[0]:', Y_train_feats[0]

	max_X_len = len(X_train_feats[0])
	max_Y_len = len(Y_train_feats[0])
	num_vocab_words = len(words_to_vecs) + 1
	
	print 'Compiling model...'
	model = Sequential()
	model.add(Embedding(num_vocab_words, GLOVE_DIM, input_length=max_X_len, weights=[embedding_matrix]))	
	model.add(recurrent.SimpleRNN(HIDDEN_SIZE))
	model.add(RepeatVector(max_Y_len))
	model.add(recurrent.SimpleRNN(HIDDEN_SIZE, return_sequences=True))
	model.add(TimeDistributedDense(num_vocab_words))
	model.add(Activation('softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam')


if __name__ == '__main__':
	main()