import sys, os

def main(argv):

    if len(argv) == 0:
        print('You must specify the data directory')

    vocabfile = 'vocab.txt'
    if len(argv) > 1:
        vocabfile = argv[1]

    path = argv[0]
    path = path[:-1] if path[-1] == '/' else path
    files = [f for f in os.listdir(path) if f[0] != '.']
    vocabs = set()
    for i in files:
        with open(path+'/'+i) as f:
            for line in f.readlines():
                for word in line.strip().split():
                    vocabs.add(word)
    with open(vocabfile, 'w') as f:
        for i in vocabs:
            f.write(i+'\n')

if __name__ == '__main__':
    main(sys.argv[1:])