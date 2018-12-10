
#   advent/2018/day09.py

import re
from collections import defaultdict, deque

##############################

def initialize():
    return deque([0]), defaultdict(int)

##############################

def game(num_players, max_value):
    marbles, score = initialize()
    for i in range(max_value // 23):
        for j in range(1, 23):
            marbles.rotate(-2)
            marbles.appendleft(23 * i + j)
        marbles.rotate(7)
        score[(23 * i) % num_players] += 23 * (i + 1) + marbles.popleft()
    return max(score.values())

##############################

if __name__ == '__main__':

    with open('data/09.txt') as f:
        s = f.read()
        num_players = int(re.search(r'(\d*) players', s).group(1))
        max_value = int(re.search(r'(\d*) points', s).group(1))

    print(game(num_players, max_value))
    print(game(num_players, 100 * max_value))
