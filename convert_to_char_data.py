def convert_to_chars(filename):
    f = open(filename, 'r')
    g = open(filename + '_char', 'w')
    for line in f:
        result = []
        for char in line:
            if char == ' ': result.append('_')
            elif char == '\n': continue
            else: result.append(char)
        result_string = ' '.join(result)
        result_string += '\n'
        g.write(result_string)
    f.close()
    g.close()



convert_to_chars('nmt.matlab/data/train.180k.premise_contr')            
convert_to_chars('nmt.matlab/data/train.180k.hypothesis_contr')
convert_to_chars('nmt.matlab/data/valid.10k.premise_contr')
convert_to_chars('nmt.matlab/data/valid.10k.hypothesis_contr')
convert_to_chars('nmt.matlab/data/test.10k.premise_contr')
convert_to_chars('nmt.matlab/data/test.10k.hypothesis_contr')
print 'Done!'
