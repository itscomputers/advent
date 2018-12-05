
#   advent/2018/01.py

from itertools import cycle

##############################

def find_first_repeat(data):
    sums = set()
    d = cycle(data)
    curr_sum = 0
    while True:
        if curr_sum in sums:
            return curr_sum
        sums.add(curr_sum)
        curr_sum += next(d)

##############################

if __name__ == '__main__':

    with open('data/01.txt') as f:
        data = [int(x.rstrip('\n')) for x in f.readlines()]

    print(sum(data))
    print(find_first_repeat(data))
