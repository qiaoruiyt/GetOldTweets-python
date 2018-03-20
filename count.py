import os

posfile = 'id-pos'
negfile = 'id-neg'
pos_count = 0
neg_count = 0

files = os.listdir()
for i in files:
    if posfile in i:
        with open(i) as f:
            for line in i.readlines():
                pos_count += 1
    elif negfile in i:
        with open(i) as f:
            for line in i.readlines():
                neg_count += 1
print(pos_count)
print(neg_count)
