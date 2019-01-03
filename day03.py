
#   advent/2018/day03.py

from collections import defaultdict
from itertools import product
import re

#=============================

def load(filename='data/03.txt'):
    with open(filename) as f:
        return parse(f.readlines())

#-----------------------------

def parse(data):
    id_pattern = re.compile(r'#(\d*)')
    coords_pattern = re.compile(r'(\d*),(\d*)')
    size_pattern = re.compile(r'(\d*)x(\d*)')
    def line_parse(line):
        key = int(id_pattern.search(line).group(1))
        coords = tuple(int(x) for x in \
                coords_pattern.search(line).group(1,2))
        size = tuple(int(x) for x in \
                size_pattern.search(line).group(1,2))
        return key, coords, size

    return { key : [coords, size] \
            for key, coords, size in [line_parse(line) for line in data]}

#=============================

def rectangle(array):
    coords, size = array
    cx, cy = coords
    sx, sy = size
    return [(cx + i, cy + j) for i, j in product(range(sx), range(sy))]

#-----------------------------

def process_claims(data):
    conflict_free = list()
    claims = defaultdict(list)
    for key, value in data.items():
        clean = True 
        for coord in rectangle(value):
            if coord in claims:
                if len(claims[coord]) == 1:
                    if claims[coord][0] in conflict_free:
                        conflict_free.remove(claims[coord][0])
                    if key in conflict_free:
                        conflict_free.remove(key)
                clean = False
            claims[coord].append(key)
        if clean:
            conflict_free.append(key)
    return conflict_free, claims

#=============================

def run(data):
    conflict_free, claims = process_claims(data)
    part1 = sum(1 for ids in claims.values() if len(ids) > 1)
    assert(len(conflict_free) == 1)
    part2 = conflict_free[0]
    return part1, part2

#-----------------------------

def test():
    print('\ntests:')
    part1, part2 = run(load('test/03.txt'))
    print('part 1: passed {} / 1'.format(1 * (part1 == 4)))
    print('part 2: passed {} / 1'.format(1 * (part2 == 3)))

#-----------------------------

def main():
    print('\nmain problem:')
    part1, part2 = run(load())
    print('part 1: squares = {}'.format(part1))
    print('part 2: id = {}'.format(part2))

#=============================

if __name__ == '__main__':

    print('\nproblem 3')
    test()
    main()
    print()
