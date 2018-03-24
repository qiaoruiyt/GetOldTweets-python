import os, sys

def main(argv):

    if len(argv) == 0:
        print('You must specify the data directory')

    posfile = 'pos'
    negfile = 'neg'
    pos_count = 0
    neg_count = 0

    path = argv[0]
    files = [path + '/' + i for i in os.listdir(path)]
    for i in files:
        if posfile in i:
            with open(i) as f:
                for line in f.readlines():
                    pos_count += 1
        elif negfile in i:
            with open(i) as f:
                for line in f.readlines():
                    neg_count += 1
    print(pos_count)
    print(neg_count)


if __name__ == '__main__':
    main(sys.argv[1:])