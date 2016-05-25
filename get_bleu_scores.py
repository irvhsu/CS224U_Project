from constants import *
from nltk.translate import bleu_score
import sys
'''
Function: get_bleu_scores
-------------------------
Takes in a pair of files -- one containing the ground truth hypotheses, and the other containing the
generated hypotheses. Computes the BLEU score for each pair of sentences, and outputs the average
BLEU score at the end.
'''
def get_bleu_scores(infile1, infile2, n=1):
    print "\nComputing BLEU score for n={}...".format(n)
    f1 = open(infile1)
    f2 = open(infile2)

    sentences_f1 = f1.readlines()
    sentences_f2 = f2.readlines()

    bleu_scores = []

    sentence_pairs = zip(sentences_f1, sentences_f2)

    for pair in sentence_pairs:
        # Ground truth hypothesis
        reference = pair[0][:-1]
        # Generated hypothesis
        hypothesis = pair[1][:-1]

        score = bleu_score._modified_precision([reference], hypothesis, n)
        bleu_scores.append(float(score))

    avg_bleu_score = sum(bleu_scores) / float(len(bleu_scores))
    print "Average BLEU score: {}\n".format(avg_bleu_score)

if __name__ == '__main__':

    infile1 = "milestone_outputs/" + sys.argv[1] + '_hypothesis.txt'
    infile2 = "milestone_outputs/" + sys.argv[2] + '_' + sys.argv[1] + '_results.txt'

    get_bleu_scores(infile1, infile2, n=1)
    get_bleu_scores(infile1, infile2, n=2)
