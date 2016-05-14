import re
import pickle

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
	# counter = 0
	for line in f:
		# if counter == 20: break
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
		# counter += 1
	f.close()
	# Pickle file name
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
		if char == "'": sentence = sentence[:index] + ' ' + sentence[index:] 
	return sentence


if __name__ == '__main__':
	read_snli_data('snli_1.0/snli_1.0_train.txt')

