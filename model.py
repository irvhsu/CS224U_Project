from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, TimeDistributedDense, RepeatVector
from keras.layers.embeddings import Embedding
from keras.layers import recurrent
from constants import *


class ModelDefinition:

	def __init__(self, embedding_matrix, num_vocab_words, output_vocab_len, max_X_len, max_Y_len):
		self.embedding_matrix = embedding_matrix
		self.num_vocab_words = num_vocab_words
		self.output_vocab_len = output_vocab_len
		self.max_X_len = max_X_len
		self.max_Y_len = max_Y_len
		self.model_defs = {}
		self.define_RNN()
		self.define_GRU()
		self.define_LSTM()

	def define_RNN(self):
		model = Sequential()
		model.add(Embedding(self.num_vocab_words, GLOVE_DIM, input_length=self.max_X_len, weights=[self.embedding_matrix], mask_zero=True))	
		model.add(recurrent.SimpleRNN(HIDDEN_SIZE))
		model.add(RepeatVector(self.max_Y_len))
		for _ in range(LAYERS):
			model.add(recurrent.SimpleRNN(HIDDEN_SIZE, return_sequences=True))
		model.add(TimeDistributedDense(self.output_vocab_len))
		model.add(Activation('softmax'))
		self.model_defs['rnn'] = model

	def define_GRU(self):
		model = Sequential()
		model.add(Embedding(self.num_vocab_words, GLOVE_DIM, input_length=self.max_X_len, weights=[self.embedding_matrix], mask_zero=True))	
		model.add(recurrent.GRU(HIDDEN_SIZE))
		model.add(RepeatVector(self.max_Y_len))
		for _ in range(LAYERS):
			model.add(recurrent.GRU(HIDDEN_SIZE, return_sequences=True))
		model.add(TimeDistributedDense(self.output_vocab_len))
		model.add(Activation('softmax'))
		self.model_defs['gru'] = model

	def define_LSTM(self):
		model = Sequential()
		model.add(Embedding(self.num_vocab_words, GLOVE_DIM, input_length=self.max_X_len, weights=[self.embedding_matrix], mask_zero=True))	
		model.add(recurrent.LSTM(HIDDEN_SIZE))
		model.add(RepeatVector(self.max_Y_len))
		for _ in range(LAYERS):
			model.add(recurrent.LSTM(HIDDEN_SIZE, return_sequences=True))
		model.add(TimeDistributedDense(self.output_vocab_len))
		model.add(Activation('softmax'))
		self.model_defs['lstm'] = model
