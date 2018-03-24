import sys, os, codecs
from nltk.tokenize import TweetTokenizer

def main(argv):

    if len(argv) == 0:
        print('You must specify the data directory')

    path = argv[0]
    path = path[:-1] if path[-1] == '/' else path

    tokenized_dir = 'tokenized'
    if len(argv) > 1:
        tokenized_dir = argv[1][:-1] if argv[1][-1] == '/' else argv[1]

    if not os.path.exists(tokenized_dir):
        os.makedirs(tokenized_dir)

    files = [f for f in os.listdir(path) if f[0] != '.']

    tt = TweetTokenizer()
    for i in files:
        print("Tokenizing", i)
        with codecs.open(path+'/'+i, 'r', 'utf-8') as f:
            with codecs.open(tokenized_dir+'/'+i, 'w', 'utf-8') as fout:
                for line in f.readlines():
                    tokenized_line = tt.tokenize(line)
                    fout.write(' '.join(tokenized_line)+'\n')

if __name__ == '__main__':
    main(sys.argv[1:])