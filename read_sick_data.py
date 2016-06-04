import re
import pickle
from constants import *
import enchant
from autocorrect import spell

d = enchant.Dict("en_US")
typos = set()

'''
Function: read_sick_data
------------------------
Reads the SICK data from the given filename
into a list of tuples, where the first element is
the premise, and the second is the hypothesis.
If get_bidirectional_entailments=True, we only
get entailments where A entails B and B entails A.
'''
def read_sick_data(filename, get_bidirectional_entailments=True):
    print 'Reading in data from ' + filename + '...'
    f = open(filename)
    data_list = []
    for line in f:
        # Split input line by tabs
        split_line = line.split('\t')
        # Only look at entailments
        entailment_label = split_line[3]
        if entailment_label != 'ENTAILMENT': continue
        if get_bidirectional_entailments:
            # Forward entailment satisfied by default; check reverse entailment
            entailment_BA = split_line[6]
            if entailment_BA != 'B_entails_A': continue

        # Put spaces before punctuation marks
        premise = format_sent(split_line[1])
        hypothesis = format_sent(split_line[2])
        # Add to growing data list
        data_list.append((premise, hypothesis))
    f.close()

    print data_list

    # Pickle file name
    pickle_filename = filename.split('.txt')[0]
    # If the filename only contains bidirectional entailments
    if get_bidirectional_entailments: pickle_filename += '_bidirectional'
    pickle_filename += '_data.pickle'

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
def format_sent(sentence, add_tags=True):
    sentence = sentence.lower()
    sentence = re.sub(r"([a-z])\-([a-z])", r"\1 \2", sentence)
    sentence = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", sentence)
    for index, char in enumerate(sentence):
        if char == "'" or char == '"': sentence = sentence[:index] + ' ' + sentence[index:]
    sentence = fix_typos(sentence)
    if add_tags:
        return '_START_ ' + sentence + ' _END_'
    return sentence


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


if __name__ == '__main__':
    print "Reading SICK data..."
    read_sick_data(SICK_DATA_FILE, True)
    read_sick_data(SICK_DATA_FILE, False)
