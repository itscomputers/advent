
#   advent/2018/day02.py

from collections import Counter

#=============================

def load(filename='data/02.txt'):
    with open(filename) as f:
        return [x.rstrip() for x in f.readlines()]

#=============================

def find_checksum(data):
    twos, threes = 0, 0
    for d in data:
        vals = set(Counter(d).values())
        if 2 in vals:
            twos += 1
        if 3 in vals:
            threes += 1
    return twos * threes

#-----------------------------

def find_similarity(data):
    for i in range(len(data[0])):
        for k, v in Counter([''.join(x[:i] + x[i+1:]) for x in data]).items():
            if v == 2:
                return k

#=============================

def test():
    print('\ntests:')
    part1 = find_checksum(load('test/02-a.txt'))
    part2 = find_similarity(load('test/02-b.txt'))
    print('part 1: passed {} / 1'.format(1 * (part1 == 12)))
    print('part 2: passed {} / 1'.format(1 * (part2 == 'fgij')))

#-----------------------------

def main():
    print('\nmain problem:')
    data = load()
    print('part 1: checksum = {}'.format(find_checksum(data)))
    print('part 2: similarity = {}'.format(find_similarity(data)))

#=============================

if __name__ == '__main__':

    print('\nproblem 1')
    test()
    main()
    print()
