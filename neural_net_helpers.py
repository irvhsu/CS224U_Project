from __future__ import print_function
import numpy as np
import pickle 
from keras.preprocessing import sequence
np.random.seed(1337)

'''
Function: addUnseenWords
------------------------
This function accepts a mapping from words to vectors, the
desired size of each vector, and a list of strings representing
training sentences. It then takes any word in X that is not
in wordsToVecs, and adds it while initializing it to a random vector.
'''
def addUnseenWords(wordsToVecs, wordVecSize, X):
	# For every article in the data
	for sentence in X:
		# For every word in the article
		for word in sentence.split():
			# If we've not seen it before, initialize a random vector.
			if word not in wordsToVecs:
				wordsToVecs[word] = 0.01*np.random.randn(wordVecSize)


'''
Function: createEmbeddingMatrix
-------------------------------
This function accepts a map from words to vectors, and a map from words
to indices, and then builds an embedding matrix such that row i of the
matrix contains the vector associated with the word at index i. 
''' 
def createEmbeddingMatrix(wordsToVecs, wordsToIndices):
	print("Creating Embedding Matrix...")
	numVocabWords = len(wordsToVecs) + 1
	# Initialize the embedding matrix
	embeddingMatrix = np.zeros([numVocabWords, len(wordsToVecs.values()[0])])
	# For every word in our dictionary
	for word in wordsToIndices:
		# Get the index and vector
		index = wordsToIndices[word]
		vector = wordsToVecs[word]
		# Set the appropriate element in the matrix
		embeddingMatrix[index, :] = vector
	# Return result
	return embeddingMatrix


'''
Function: loadGloveVectors
--------------------------
Given a desired dimensionality (valid values are only 50, 100, 200, 300),
this function returns a dictionary mapping every word in the Glove corpus to
its corresponding pre-trained vector. 
'''
def loadGloveVectors(nDim=100):
	print('Loading Glove Vector Embeddings...')
	wordsToVecs = {}
	filename = 'glove.6B.' + str(nDim)+'d.txt'
	f = open(filename, 'r')
	# For every line in the file
	for line in f:
		# Split the line
		split_line = line.split()
		# Get the word in question
		word = split_line[0]
		# Convert the remaining values to an np array of floats
		vector = np.array([float(x) for x in split_line[1:]])
		# Assign the vector to that word.
		wordsToVecs[word] = vector
	return wordsToVecs


'''
Function: buildDictionary
-------------------------
This helper function takes in a mapping of words to vectors,
and uses this corpus of words to map each word to an index.
It then returns this mapping as a dictionary.
'''
def buildDictionary(wordsToVecs, saveToFile=True):
	print("Mapping corpus words to indices...")
	wordsToIndices = {}
	for index, word in enumerate(wordsToVecs):
		# We use index + 1 instead of index because we want
		# to reserve the 0-th index for a padding token.
		wordsToIndices[word] = index + 1
	# Save the mappings to a file.
	if saveToFile:
		f = open('wordsToInd.p', 'wb')
		pickle.dump(wordsToIndices, f)
		f.close()
	return wordsToIndices


'''
Function: convertToIndexSequence
--------------------------------
This function takes a list of articles (strings) and returns a list 
of sequences of indices corresponding to the words in the article.
If there are any words that are not in the corpus, we ignore them.

The return value is a list of lists of indices.
'''
def convertToIndexSequence(X, wordsToIndices):
	finalResult = []
	# For every article
	for index, article in enumerate(X):
		# Split into words
		split_line = article.split()
		indexSequence = []
		# For every word
		for word in split_line:
			# If it's not in our mapping from words to indices,
			# ignore it.
			if word not in wordsToIndices:
				continue
			# Append it to the sequence
			indexSequence.append(wordsToIndices[word])
		finalResult.append(indexSequence)
	# Return the final result
	return finalResult


'''
Function: convertToOneHot
-------------------------
Given a list of labels, return a
corresponding list of one-hot vectors. 
'''
def convertToOneHot(Y):
	numClasses = len(set(Y))
	# Initialize the results. 
	result = np.zeros((len(Y), numClasses))
	# For every label in Y
	for index, label in enumerate(Y):
		result[index][label] = 1
	return result


'''
Function: breakApartInputs
--------------------------
This function takes in a list of index sequences X, a list of labels
Y, and an optional subsetSize. It then breaks X into chunks of size 
subsetSize, and duplicates Y for the necessary number of times for each
article. It then returns the final results.
'''
def breakApartInputs(X, Y, subsetSize=7):
	X_result = []
	Y_result = []
	# For every article-label pair
	for article, label in zip(X, Y):
		# For every chunk
		for i in range(0, len(article), subsetSize):
			X_result.append(article[i:i+subsetSize])
			Y_result.append(label)
	# Return result
	return X_result, Y_result


'''
Function: augmentData
---------------------
This function takes in X, a list of sequences,
and Y, a list of corresponding labels,
and augments this data by appending the reverse of
every sequence to X, and appending Y to itself. 
'''
def augmentData(X, Y):
	print('Augmenting Data...')
	X_reversed = []
	# For every sequence
	for sequence in X:
		# Reverse it
		reversedSeq = sequence[::-1]
		X_reversed.append(reversedSeq)
	# Return results
	X += X_reversed
	Y += Y
	return X, Y	


'''
Function: ensembleAccuracy
--------------------------
This function accepts an ensemble neural net model,
a given blockLength, a set of articles X (a list of
index sequences), and Y, a list of labels. It then
computes the accuracy of the model on this data.
'''
def ensembleAccuracy(model, blockLength, X, Y):
	counter = 0.0
	# For every article, label pair
	for artSequence, label in zip(X, Y):
		# Break article into chunks
		chunks = []
    	for i in range(0, len(artSequence), blockLength):
    		chunks.append(artSequence[i:i+blockLength])
    	# Pad chunks to the same length
		chunks = sequence.pad_sequences(chunks, padding='pre')
		# Predict the probabilities for each chunk
		probs = model.predict_proba(chunks, verbose=0)
		sumProbs = np.sum(probs, axis=0)
		# Compute the predicted label
		predClass = np.argmax(sumProbs)
		if predClass == label:
			counter += 1

	# Return final accuracy
	return counter/float(len(Y))	

'''
Function: ensembleProbs
--------------------------
This function accepts an ensemble neural net,
a block length, and a list of articles.
It then returns for every input sequence
the probabilities that it belongs to each
category.
'''
def ensembleProbs(model, blockLength, X):
	allProbs = []
	# For every article
	for artSequence in X:
		# Break the article into chunks
		chunks = []
		for i in range(0, len(artSequence), blockLength):
			chunks.append(artSequence[i:i+blockLength])
		# Pad chunks to same size
		chunks = sequence.pad_sequences(chunks, padding='pre', maxlen=blockLength)
		# Predict probability for each chunk
		probs = model.predict_proba(chunks, verbose=0)
		# Sum over the probability vectors
		sumProbs = np.sum(probs, axis=0)
		# Normalize and append final probabilities.
		allProbs.append(sumProbs/np.sum(sumProbs))
	return allProbs

def convertToOneHot(Y, num_words):
	# Create 3D matrix (num_sentences, num_words_per_sentence, num_vocab_words)
	result = np.zeros((Y.shape[0], Y.shape[1], num_words))
	# For every sentence
	for sent in range(Y.shape[0]):
		# For every word
		for word in range(Y.shape[1]):
			# Get the index from the index sequence
			index = Y[sent, word]
			result[sent][word][index] = 1
	return result
