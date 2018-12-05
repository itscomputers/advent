
#   advent/2018/day02.py

from collections import Counter

##############################

def find_checksum(data):
    twos, threes = 0, 0
    for d in data:
        vals = set(Counter(d).values())
        if 2 in vals:
            twos += 1
        if 3 in vals:
            threes += 1
    return twos * threes

##############################

def find_similarity(data):
    for i in range(len(data[0])):
        for k, v in Counter([''.join(x[:i] + x[i+1:]) for x in data]).items():
            if v == 2:
                return k

##############################

if __name__ == '__main__':

    with open('data/02.txt') as f:
        data = [x.rstrip('\n') for x in f.readlines()]

    print(find_checksum(data))
    print(find_similarity(data))
