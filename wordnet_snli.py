from nltk.corpus import wordnet as wn
from nltk.tree import Tree
import numpy as np
import json
from __future__ import print_function


test_string = """(ROOT (S (NP (DT This) (NN church) (NN choir)) (VP (VBZ sings) (PP (TO to) (NP (DT the) 
(NNS masses))) (SBAR (IN as) (S (NP (PRP they)) (VP (VBP sing) (NP (JJ joyous) (NNS songs)) 
(PP (IN from) (NP (NP (DT the) (NN book)) (PP (IN at) (NP (DT a) (NN church))))))))) (. .)))"""
b = str2tree(test_string)

def str2tree(s):
    """Map str `s` to an `nltk.tree.Tree` instance. The assumption is that 
    `s` represents a standard Penn-style tree."""
    return Tree.fromstring(s)    

lines_read = 0
with open('train_wordnet_para.jsonl', 'a') as f:
    with open('snli_1.0/snli_1.0_train.jsonl') as data_file:
        for line in data_file:
            data = json.loads(line)
            if data['gold_label'] != 'entailment':
                continue
            lines_read += 1
            if lines_read > 100:
                break

            text_string = data["sentence1_parse"]
            text_tree = str2tree(text_string)
            pos_pairs = text_tree.pos()
            #word_pos = b.pos()
            #print(*myList, sep='\n')

            print(*[pair[0] for pair in pos_pairs], sep = ' ')
            f.write(data["sentence1"] + '\n')
            for i, (word, pos) in enumerate(pos_pairs):
                if pos == "NN":
                    synsets = wn.synsets(word, 'n')
                    if len(synsets) == 0:
                        continue #Wordnet can't find this word!

                    hypernyms = wn.synsets(word, 'n')[0].hypernyms()
                    if len(hypernyms) > 0:
                        pos_pairs[i] = (hypernyms[0].lemma_names()[0], pos_pairs[i][1])
                if pos.startswith("VB"):
                    synsets = wn.synsets(word, 'v')
                    if len(synsets) == 0:
                        continue #Wordnet can't find this word!
                    entailments = wn.synsets(word, 'v')[0].entailments()
                    if len(entailments) > 0:
                        pos_pairs[i] = (entailments[0].lemma_names()[0], pos_pairs[i][1])
                    # print(wn.synsets(word, 'v')[0].entailments())
                    # print([h for ss in wn.synsets(word, 'v') for h in ss.entailments()])
                    # hyp1 = 
                # print word, pos
            print(*[pair[0] for pair in pos_pairs], sep = ' ')
            output = ' '.join(str(pair[0]) for pair in pos_pairs)
            f.write(output + '\n')
            print(data["sentence2"])
            f.write(data["sentence2"] + '\n\n')
            print("\n")

