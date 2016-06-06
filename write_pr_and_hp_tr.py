from constants import *
from read_snli_data import *

'''
Function: process_tr_data
---------------------------
Reads the translation data from the given filename
and writes the premises and hypotheses of the
entailments into separate output files.
'''
def process_tr_data(infile):
    outfile_pr = 'translate.premise'
    outfile_hp = 'translate.hypothesis'

    print 'Reading in data from ' + infile + '...'
    f = open(infile, 'r')
    # List of premises
    premise_list = []
    # List of hypotheses
    hypothesis_list = []
    for line in f:
        # Split input line by tabs
        try:
            split_line = line.split('\t')
            premise = format_sent(split_line[0], False)
            hypothesis = format_sent(split_line[1], False)
        except:
            continue
        # Add to growing premise and hypothesis lists
        premise_list.append(premise)
        hypothesis_list.append(hypothesis)
    f.close()

    # Write the premises and hypotheses to their corresponding output files
    write_to_file(outfile_pr, premise_list)
    write_to_file(outfile_hp, hypothesis_list)

    print 'Done!'


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
    process_tr_data('train_para.txt')
