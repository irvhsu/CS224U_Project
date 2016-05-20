import numpy as np
import sys

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, TimeDistributedDense, RepeatVector
from keras.layers.embeddings import Embedding
from keras.layers import recurrent
from read_snli_data import *
from constants import *
from neural_net_helpers import *
from model import ModelDefinition

def main(model_name):
	# Read pickled training and dev files
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

	# Get final embedding matrix
	embedding_matrix = createEmbeddingMatrix(words_to_vecs, words_to_indices)

	print("Converting input sequences to lists of indices...")
	# Convert the input sentences to lists of lists of indices
	X_feats = convertToIndexSequence(X_train + X_dev, words_to_indices)

	print("Converting output sequences to lists of indices...")
	# Convert the input sentences to lists of lists of indices
	Y_seq, Y_words_to_inds, Y_inds_to_words, output_vocab_len = convertYsToIndexSequence(Y_train + Y_dev)

	print("Padding sequences to the same length...")
	X_feats = sequence.pad_sequences(X_feats, padding='pre')
	X_train_feats = X_feats[:num_train]
	X_dev_feats = X_feats[num_train:]

	Y_seq = sequence.pad_sequences(Y_seq, padding='post')
	Y_train_seq = Y_seq[:num_train]
	Y_dev_seq = Y_seq[num_train:]


	# Get max lengths for efficiency
	max_X_len = len(X_train_feats[0])
	max_Y_len = len(Y_train_seq[0])
	num_vocab_words = len(words_to_vecs) + 1
	
	print 'Compiling ' + model_name + ' model...'
	model = ModelDefinition(embedding_matrix, num_vocab_words, \
					output_vocab_len, max_X_len, max_Y_len).model_defs[model_name]

	model.compile(loss='categorical_crossentropy', optimizer='adam')
	for epoch in range(NUM_EPOCHS):
		print 'Starting Epoch ' + str(epoch)
		num_iters = int(num_train/BATCH_SIZE) + 1
		for iteration in range(num_iters):
			print 'Iteration ' + str(iteration)
			all_indices = np.array(range(num_train))
			batch_inds = np.random.choice(all_indices, size=[BATCH_SIZE], replace=False)
			X_batch = X_train_feats[batch_inds]
			Y_batch = Y_train_seq[batch_inds]
			Y_one_hot = convertToOneHot(Y_batch, output_vocab_len)
			model.fit(X_batch, Y_one_hot, batch_size=BATCH_SIZE, nb_epoch=1, show_accuracy=True)
			if (iteration % PRINT_FREQ) == 0:
				preds = model.predict_classes(X_batch, verbose=0)
				print convert_to_word_list(preds, Y_inds_to_words) 



if __name__ == '__main__':
	main(sys.argv[1])