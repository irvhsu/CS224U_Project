import sys


def convert_from_chars(infile, outfile):
    print 'Reading from ' + infile
    print 'Writing to ' + outfile
    f = open(infile, 'r')
    g = open(outfile, 'w')
    for line in f:
        split_line = line.split()
        chars = [char if char is not '_' else ' ' for char in split_line]
        new_line = ''.join(chars) + '\n'
        g.write(new_line)
    f.close()
    g.close()


if __name__=='__main__':
    convert_from_chars(sys.argv[1], sys.argv[2])
