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

def main(model_name, test_filename):
	# Read pickled files
	test_tuples = read_pickle_file(test_filename)
	X, Y = zip(*test_tuples)

	print 'Loading JSON file...'
	json_file = modelName + '.json'
	model = model_from_json(open(json_file).read())

	print 'Loading weights...'
	model.load_weights(modelName + '.h5')

	print 'Loading wordsToInd...'
	f = open('wordsToInd.p', 'rb')
	wordsToIndices = pickle.load(f)
	f.close()

	print 'Loading Y_inds_to_words...'
	g = open('Y_inds_to_words.p', 'rb')
	Y_inds_to_words = pickle.load(g)
	g.close()
	max_length = model.layers[0].input_length

	print("Converting input sequences to lists of indices...")
	# Convert the input sentences to lists of lists of indices
	X_feats = convertToIndexSequence(X, words_to_indices)
	X_feats = sequence.pad_sequences(X_feats, padding='pre', maxlen=max_length)

	for i, feat in enumerate(X_feats):
		print 'Example ' + str(i)
		example = np.array([X_feats[i, :]])
		preds = model.predict_classes(X_batch, verbose=0)
		print convert_to_word_list(preds, Y_inds_to_words)


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
