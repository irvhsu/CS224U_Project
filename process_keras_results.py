import sys

def process(filename, new_filename):
    f = open(filename, 'r')
    g = open(new_filename, 'w')
    counter = 0
    for line in f:
        counter += 1
        split_line = line.split()
        if split_line[-1] == '_END_':
            split_line = split_line[:-1]
        new_line = ' '.join(split_line)
        g.write(new_line + '\n')
        if (counter % 10) == 0:
            print str(counter)

    f.close()
    g.close()



if __name__ == '__main__':
    process(sys.argv[1], sys.argv[2])
        
