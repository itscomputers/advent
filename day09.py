
#   advent/2018/day09.py

import re
from collections import defaultdict, deque

#=============================

def load(filename='data/09.txt'):
    with open(filename) as f:
        return parse(f.read())

#-----------------------------

def parse(data):
    num_players = int(re.search(r'(\d+) players', data).group(1))
    max_value = int(re.search(r'(\d+) points', data).group(1))
    return num_players, max_value

#=============================

def initialize():
    return deque([0]), defaultdict(int)

#-----------------------------

def game(num_players, max_value):
    marbles, score = initialize()
    for i in range(max_value // 23):
        for j in range(1, 23):
            marbles.rotate(-2)
            marbles.appendleft(23 * i + j)
        marbles.rotate(7)
        score[(23 * i) % num_players] += 23 * (i + 1) + marbles.popleft()
    return max(score.values())

#=============================

def test(ch):
    results = {
        'a' : 8317,
        'b' : 146373,
        'c' : 2764,
        'd' : 54718,
        'e' : 37305
    }
    return game(*load('test/09-{}.txt'.format(ch))) == results[ch]

#-----------------------------

def main():
    num_players, max_value = load()
    print('\nmain problem:')
    print('part 1: winning score = {}'.format(game(num_players, max_value)))
    print('part 2: winning score = {}'.format(game(num_players, 100*max_value)))

##############################

if __name__ == '__main__':
    print('part 1 tests: passed {} / {}'.format(
        sum(1 * test(ch) for ch in 'abcde'), len('abcde')))

    main()
