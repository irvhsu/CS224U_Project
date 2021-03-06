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
    # weights = tuple([1/float(n) for i in range(n)])
    # print 'corpus_bleu: ', bleu_score.corpus_bleu(sentences_f1, sentences_f2, weights=weights)

    bleu_scores = []

    sentence_pairs = zip(sentences_f1, sentences_f2)

    for pair in sentence_pairs:
        # Ground truth hypothesis
        reference = pair[0][:-1]
        # Generated hypothesis
        hypothesis = pair[1][:-1]

        score = bleu_score.modified_precision([reference], hypothesis, n)
        bleu_scores.append(float(score))

    avg_bleu_score = sum(bleu_scores) / float(len(bleu_scores))
    print "Average BLEU score: {}\n".format(avg_bleu_score)

if __name__ == '__main__':
    '''
    Argument 1 is either 'train', 'valid', or 'test'. Argument 2 is the model name.
    '''
    infile1 = 'contradictions/' + sys.argv[1] + '_hypothesis.txt'
    infile2 = 'contradictions/' + sys.argv[2] + '/translations_' + sys.argv[1] + '.txt'

    # get_bleu_scores(infile1, infile2, n=1)
    get_bleu_scores(infile1, infile2, n=2)
    # get_bleu_scores(infile1, infile2, n=3)
    # get_bleu_scores(infile1, infile2, n=4)
