import sys
from constants import *

'''
Function: get_entailment_accuracies
-----------------------------------
Takes in a pair of files -- one containing the original premises, and the other containing the
generated hypotheses. Each line in the first file corresponds to each line in the second file.
Outputs each pair of lines one at a time, and for each pair, prompts user to enter in "yes" or "no"
depending on whether or not the generated hypothesis is a valid entailment of the original premise.
Reports the accuracy at the end.
'''
def get_entailment_accuracies(infile1, infile2):
    f1 = open(infile1)
    f2 = open(infile2)

    sentences_f1 = f1.readlines()
    sentences_f2 = f2.readlines()

    sentence_pairs = zip(sentences_f1, sentences_f2)

    valid_responses = set(['yes', 'y', 'no', 'n'])

    # Counter for number of valid responses
    num_valid = 0

    # Counter for number of total sentences
    num_sentences = 0

    for i, pair in enumerate(sentence_pairs):
        if i not in SAMPLE_INDS: continue
        sentence_1 = pair[0][:-1]
        sentence_2 = pair[1][:-1]
        period_location = sentence_2.find('.')
        if period_location >= 0: sentence_2 = sentence_2[:period_location + 1]
        print '\nSentence ' + str(num_sentences + 1) + '/' + str(len(SAMPLE_INDS))
        print "ORIGINAL PREMISE: {}".format(sentence_1)
        print "GENERATED HYPOTHESIS: {}".format(sentence_2)

        while True:
            response = raw_input("Valid entailment? (y/n) ").lower()
            if response not in valid_responses:
                print "Please respond with 'yes' or 'no' (or 'y' or 'n').\n"
            else: break

        if response[0] == 'y':
            num_valid += 1
        num_sentences += 1

    final_accuracy = float(num_valid) / num_sentences

    print "\nDone!"
    print "Final accuracy: {}\n".format(final_accuracy)


'''
Argument 1 is either 'dev' or 'test'. Argument 2 is either 'model1', 'model2', or 'model3'.
'''
if __name__ == '__main__':
    infile1 = "milestone_outputs/" + sys.argv[1] + '_premise.txt'
    infile2 = "milestone_outputs/" + sys.argv[2] + '_' + sys.argv[1] + '_results.txt'
    get_entailment_accuracies(infile1, infile2)
