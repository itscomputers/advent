
#   advent/2018/01.py

from itertools import cycle

#=============================

def load(filename='data/01.txt'):
    with open(filename) as f:
        return [int(x) for x in f.readlines()]

#=============================

def find_first_repeat(data):
    sums = set()
    d = cycle(data)
    curr_sum = 0
    while True:
        if curr_sum in sums:
            return curr_sum
        sums.add(curr_sum)
        curr_sum += next(d)

#=============================

def test1(ch):
    filename = 'test/01-{}.txt'.format(ch)
    results = {
        'a' : 3,
        'b' : 3,
        'c' : 0,
        'd' : -6
    }
    return sum(load(filename)) == results[ch]

#-----------------------------

def test2(ch):
    filename = 'test/01-{}.txt'.format(ch)
    results = {
        'e' : 0,
        'f' : 10,
        'g' : 5,
        'h' : 14
    }
    return find_first_repeat(load(filename)) == results[ch]

#-----------------------------

def main():
    data = load()
    print('\nmain problem:')
    print('part 1: resulting frequency = {}'.format(sum(data)))
    print('part 2: first repeat = {}'.format(find_first_repeat(data)))

#=============================

if __name__ == '__main__':
    print('part 1 tests: passed {} / {}'.format(
        sum(1*test1(ch) for ch in 'abcd'),
        len('abcd')))
    print('part 2 tests: passed {} / {}'.format(
        sum(1*test2(ch) for ch in 'efgh'),
        len('efgh')))

    main()
