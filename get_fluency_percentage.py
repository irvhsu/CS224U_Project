import sys
from constants import *

'''
Function: get_fluency_percentage
--------------------------------
Takes in a file of generations, where each line corresponds to a generation. For each generation,
prompts the user to enter "yes" or "no" depending on whether or not the generation is fluent.
Reports the percent of fluent generations at the end.
'''
def get_fluency_percentage(infile):
    f = open(infile)
    generations = f.readlines()
    print "Generations: {}".format(generations)

    valid_responses = set(['yes', 'y', 'no', 'n'])

    # Counter for number of fluent generations
    num_fluent = 0

    # Counter for number of total generations
    num_generations = 0

    for i, generation in enumerate(generations):
        if i not in SAMPLE_INDS: continue
        print '\nGeneration ' + str(num_generations + 1) + '/' + str(len(SAMPLE_INDS))
        print "GENERATION: {}".format(generation)

        while True:
            response = raw_input("Fluent generation? (y/n) ").lower()
            if response not in valid_responses:
                print "Please respond with 'yes' or 'no' (or 'y' or 'n').\n"
            else: break

        if response[0] == 'y':
            num_fluent += 1
        num_generations += 1

    assert(num_generations > 0)
    fluency_percentage = float(num_fluent) / num_generations

    print "\nDone!"
    print "Percent Generations that are Fluent: {}\n".format(fluency_percentage)


if __name__ == '__main__':
    infile = "test_files/hypotheses.txt"
    get_fluency_percentage(infile)
