
#   advent/2018/day03.py

from collections import defaultdict
from itertools import product

def parse(data):
    def line_parse(line):
        key, rest = line.split(' @ ')
        coords, size = rest.split(': ')
        coords = tuple(int(x) for x in coords.split(','))
        size = tuple(int(x) for x in size.split('x'))
        return key, coords, size

    return { key : [coords, size] \
            for key, coords, size in [line_parse(line) for line in data]}

##############################

def rectangle(array):
    coords, size = array
    cx, cy = coords
    sx, sy = size
    return [(cx + i, cy + j) for i, j in product(range(sx), range(sy))]

##############################

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

##############################

if __name__ == '__main__':

    with open('data/03.txt') as f:
        data = f.readlines()

    data = parse(data)
    conflict_free, claims = process_claims(data)
    print(sum(1 for ids in claims.values() if len(ids) > 1))
    print(conflict_free[0])
    assert( len(conflict_free) == 1 )
