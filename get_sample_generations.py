import sys
from constants import *

# List of valid responses the user can enter when prompted.
VALID_RESPONSES = set(['yes', 'y', 'no', 'n'])

'''
Function: get_sample_generations
--------------------------------
Takes in a directory name and a dataset (validation, test),
and outputs the generations from each model for each premise.
'''
def get_sample_generations(dirname, dataset):
    assert(dirname == 'reverse_ent' or dirname == 'contradiction')
    assert(dataset == 'valid' or dataset == 'test')

    reference_file = dirname + '/' + dataset
    if dirname == 'reverse_ent':
        reference_file += '_hypothesis.txt'
    else:
        # For contradictions, use the premise file
        reference_file += '_premise.txt'

    models = ['beam_search', 'output_aware', 'glob_attn', 'loc_attn', 'char_model']
    # Path to the translation file for each model.
    model_filenames = [dirname + '/' + model + '/translations_' + dataset + '.txt' for model in models]

    # List where each item is a list of generations from each model.
    all_generations = []

    f = open(reference_file)
    premises = f.readlines()

    for model_filename in model_filenames:
        model_file_descriptor = open(model_filename)
        generations = model_file_descriptor.readlines()
        all_generations.append(generations)

    for i, premise in enumerate(premises):
        print '\nPremise ' + str(i + 1)
        print 'PREMISE: {}'.format(premise)

        while True:
            response = raw_input("Show generations from each model? (y/n) ").lower()
            if response not in VALID_RESPONSES:
                print "Please respond with 'yes' or 'no' (or 'y' or 'n').\n"
            else:
                break
        if response[0] == 'y':
            for j, model_generations in enumerate(all_generations):
                # Get generations for each model
                model_generation = model_generations[i]
                print '\n' + str(models[j]).upper() + ': {}'.format(model_generation)
        else:
            break


    print "\nDone!"

'''
Argument 1 is either 'reverse_ent' or 'contradictions'. Argument 2 is either 'valid' or 'test
'''
if __name__ == '__main__':
    'Getting sample generations...'
    dirname = sys.argv[1]
    dataset = sys.argv[2]
    get_sample_generations(dirname, dataset)
