import editdistance
import enchant
import re
from constants import *
from autocorrect import spell

d = enchant.Dict("en_US")
typos = set()

'''
Function: process_ppdb_data
---------------------------
Reads the PPDB data from the given filename
and writes the premises and hypotheses of the
entailments into separate output files.
'''


def process_ppdb_data(infile):
    outfile_pr = infile + '.premise'
    outfile_hp = infile + '.hypothesis'

    print 'Reading in data from ' + infile + '...'
    f = open(infile, 'r')
    # List of premises
    premise_list = []
    # List of hypotheses
    hypothesis_list = []
    count = 0
    for line in f:
        # Split input line by tabs
        split_line = line.split('|||')
        # Put spaces before punctuation marks
        premise = split_line[1]
        hypothesis = split_line[2]

        # Only accept pair if all the checks pass
        if accept_pair(premise, hypothesis):
            # Add to growing premise and hypothesis lists
            premise_list.append(premise)
            hypothesis_list.append(hypothesis)
        count += 1
        if count == 1000000:
            break
    f.close()

    # Write the premises and hypotheses to their corresponding output files
    write_to_file(outfile_pr, premise_list)
    write_to_file(outfile_hp, hypothesis_list)

    print 'Done!'


'''
Function: accept_pair
---------------------
Performs a series of checks to determine whether or not the
given (premise, hypothesis) pair should be accepted. Checks include
whether the premise and hypothesis are sufficiently different by
edit distance, whether the pair consists only of valid words in the
English dictionary, and whether the pair consist only of alphanumerical
characters.
'''
def accept_pair(premise, hypothesis):
    if not d.check(premise) or not str.isalnum(premise):
        return False
    threshold = min(len(premise), len(hypothesis), 4)
    edit_distance = editdistance.eval(premise, hypothesis)
    if edit_distance < threshold:
        return False
    return True



'''
Function: write_to_file
-----------------------
Writes the data in the given list to the given output file,
line by line.
'''


def write_to_file(outfile, data_list):
    f = open(outfile, 'w')
    for sent in data_list:
        f.write(sent + '\n')
    f.close()


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
    print "Processing PPDB small file data..."
    process_ppdb_data(PPDB_S_FILE)