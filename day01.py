
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

def test():
    print('\ntests:')
    print('part 1: passed {} / {}'.format(
        sum(map(lambda x, y: x == y, 
            (sum(load('test/01-{}.txt'.format(ch))) for ch in 'abcd'), 
            [3, 3, 0, -6])),
        len('abcd')))
    print('part 2: passed {} / {}'.format(
        sum(map(lambda x, y: x == y,
            (find_first_repeat(load('test/01-{}.txt'.format(ch))) \
                    for ch in 'efgh'),
            [0, 10, 5, 14])),
        len('efgh')))
    
#-----------------------------

def main():
    print('\nmain problem:')
    print('part 1: resulting frequency = {}'.format(sum(load())))
    print('part 2: first repeat = {}'.format(find_first_repeat(load())))

#=============================

if __name__ == '__main__':

    print('\nproblem 1')
    test()
    main()
    print()
