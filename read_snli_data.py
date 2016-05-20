import re
import pickle
from constants import *
import enchant
from autocorrect import spell

d = enchant.Dict("en_US")
typos = set()
# typo_sents = set()

'''
Function: read_snli_data
------------------------
Reads the snli data from the given filename
into a list of tuples, where the first element is
the premise, and the second is the hypothesis.
'''
def read_snli_data(filename):
	print 'Reading in data from ' + filename + '...'
	f = open(filename)
	data_list = []
	for line in f:
		# Split input line by tabs
		split_line = line.split('\t')
		# Only look at entailments
		gold_label = split_line[0]
		if gold_label != 'entailment': continue
		# Put spaces before punctuation marks
		premise = format_sent(split_line[5])
		hypothesis = format_sent(split_line[6])
		# Add to growing data list
		data_list.append((premise, hypothesis))
	f.close()
	# Pickle file name
	print data_list[100]
	pickle_filename = filename.split('.txt')[0] + '_data.pickle'
	print 'Writing data to ' + pickle_filename + '...'
	# Write data in to pickle file, and close
	pf = open(pickle_filename, 'wb')
	pickle.dump(data_list, pf)
	pf.close()
	print 'Done!'

'''
Function: format_sent
---------------------
Formats an input sentence to convert to lower case, and
put a space before every punctuation mark.
'''
def format_sent(sentence):
	sentence = sentence.lower()
	sentence = re.sub(r"([a-z])\-([a-z])", r"\1 \2", sentence)
	sentence = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", sentence)
	for index, char in enumerate(sentence):
		if char == "'" or char == '"': sentence = sentence[:index] + ' ' + sentence[index:] 
	sentence = fix_typos(sentence)
	return '_START_ ' + sentence + ' _END_'

'''
Function: fix_typos
---------------------
Checks every word in the sentence for typos.
If it finds one, it replaces it with an
auto-correction.
'''
def fix_typos(sentence):
	typo_list = []
	split_sent = sentence.split()
	for i, token in enumerate(split_sent):
		if not d.check(token) and str.isalnum(token):
			split_sent[i] = spell(token).lower()
	return ' '.join(split_sent)


'''
Function: read_pickle_file
--------------------------
Reads pickled data from filename and returns 
the result.
'''
def read_pickle_file(filename):
	f = open(filename, 'rb')
	result = pickle.load(f)
	f.close()
	return result

if __name__ == '__main__':
	print "Reading training data..."
	read_snli_data(TRAIN_FILE)
	# print 'There are ' + str(len(typos)) + ' typos in the training set.'
	# for pairs in typos:
	# 	typo = pairs[0]
	# 	sent = pairs[1]
	# 	print typo 
	# 	print spell(typo)
	# 	print sent
	# typos.clear()
	print "Reading dev data..."
	read_snli_data(DEV_FILE)
	# print 'There are ' + str(len(typos)) + ' typos in the dev set.'
	# typos.clear()
	print "Reading test data..."
	read_snli_data(TEST_FILE)
	# print 'There are ' + str(len(typos)) + ' typos in the test set.'

