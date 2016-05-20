from constants import *
from read_snli_data import *

'''
Function: process_snli_data
---------------------------
Reads the snli data from the given filename
and writes the premises and hypotheses of the
entailments into separate output files.
'''


def process_snli_data(infile):
    size = '180k' if 'train' in infile else '10k'
    prefix = infile.split('.txt')[0]
    outfile_pr = prefix + size + '.premise'
    outfile_hp = prefix + size + '.hypothesis'

    print 'Reading in data from ' + infile + '...'
    f = open(infile, 'r')
    # List of premises
    premise_list = []
    # List of hypotheses
    hypothesis_list = []
    for line in f:
        # Split input line by tabs
        split_line = line.split('\t')
        # Only look at entailments
        gold_label = split_line[0]
        if gold_label != 'entailment': continue
        # Put spaces before punctuation marks
        premise = format_sent(split_line[5], False)
        hypothesis = format_sent(split_line[6], False)

        # Add to growing premise and hypothesis lists
        premise_list.append(premise)
        hypothesis_list.append(hypothesis)
        # Write premise and hypothesis to separate files
    f.close()

    # Write the premises and hypotheses to their corresponding output files
    write_to_file(outfile_pr, premise_list)
    write_to_file(outfile_hp, hypothesis_list)


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


if __name__ == '__main__':
    print "Processing training data..."
    process_snli_data(TRAIN_FILE)

    print "Processing dev data..."
    process_snli_data(DEV_FILE)

    print "Processing test data..."
    process_snli_data(TEST_FILE)
