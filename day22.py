
#   advent/2018/day22.py

import re
from functools import reduce
from itertools import product
from heapq import heappush, heappop

#=============================

def load(filename='data/22.txt'):
    with open(filename) as f:
        return parse([x.rstrip() for x in f.readlines()])

#-----------------------------

def parse(data):
    for line in data:
        if re.search(r'depth: (\d+)', line):
            depth = int(re.search(r'depth: (\d+)', line).group(1))
        if re.search(r'target: (\d+),(\d+)', line):
            target = tuple(map(lambda x: int(x),
                re.search(r'target: (\d+),(\d+)', line).group(1,2)))
    return depth, target

#=============================

def build_map(depth, target, mul_x, mul_y, mod):
    mp = dict()
    for x in range(target[0] + 1):
        erosion = get_erosion(x, 0, mp, depth, mul_x, mul_y, mod)
        typ = erosion % 3
        mp[x, 0] = erosion, typ
    for y in range(target[1] + 1):
        erosion = get_erosion(0, y, mp, depth, mul_x, mul_y, mod)
        typ = erosion % 3
        mp[0, y] = erosion, typ
    for y in range(1, target[1] + 1):
        for x in range(1, target[0] + 1):
            erosion = get_erosion(x, y, mp, depth, mul_x, mul_y, mod)
            typ = erosion % 3
            mp[x, y] = erosion, typ
    mp[target] = (depth, depth % 3)
    return mp

#-----------------------------

def extend_map(x, y, mp, depth, mul_x, mul_y, mod):
    xmax, ymax = max(mp.keys())
    for i in range(xmax + 1, xmax + x + 1):
        for j in range(ymax + 1):
            erosion = get_erosion(i, j, mp, depth, mul_x, mul_y, mod)
            typ = erosion % 3
            mp[i, j] = (erosion, typ)
    for j in range(ymax + 1, ymax + y + 1):
        for i in range(xmax + x + 1):
            erosion = get_erosion(i, j, mp, depth, mul_x, mul_y, mod)
            typ = erosion % 3
            mp[i, j] = (erosion, typ)
    return mp

#-----------------------------

def print_map(mp):
    xmax, ymax = max(mp.keys())
    lines = []
    for y in range(ymax + 1):
        line = ''
        for x in range(xmax + 1):
            if mp[x, y][1] == 0:
                line += '.'
            elif mp[x, y][1] == 1:
                line += '='
            elif mp[x, y][1] == 2:
                line += '|'
        lines.append(line)
    print('\n'.join(lines))

#-----------------------------

def double_map(mp):
    return [(x, y, t) for ((x,y), t) \
            in product(mp.keys(), ['t', 'c', 'n']) \
            if compatible(mp[x,y][1], t)]

#-----------------------------

def get_erosion(x, y, mp, depth, mul_x, mul_y, mod):
    if y == 0:
        return (mul_x * x + depth) % mod
    elif x == 0:
        return (mul_y * y + depth) % mod
    else:
        return (mp[x-1, y][0] * mp[x, y-1][0] + depth) % mod

#-----------------------------

def compatible(typ, tool):
    return (typ == 0 and tool in ['t', 'c']) \
            or (typ == 1 and tool in ['c', 'n']) \
            or (typ == 2 and tool in ['t', 'n'])

#-----------------------------

def nb_dist(pt, nb, d_mp):
    if pt[:2] == nb[:2]:
        return 7
    elif pt[2] == nb[2]:
        return 1
    elif (*pt[:2], nb[2]) in d_mp or (*nb[:2], pt[2]) in d_mp:
        return 8
    else:
        return 13

#-----------------------------

def L1_dist(pt, nb):
    return sum(map(lambda x, y: abs(x - y), pt[:2], nb[:2]))

#-----------------------------

def nbhd(pt, d_mp):
    x, y = pt[:2]
    return [nb for nb in d_mp if nb != pt \
            and nb[:2] in [(x, y-1), (x, y+1), (x-1, y), (x+1, y), (x, y)]]

#-----------------------------

def a_star(d_mp, target):
    start = (0, 0, 't')
    end = (*target, 't')

    g = {start : 0}
    f = {start : L1_dist(start, end)}

    closed_set = set()
    open_set = [] 
    heappush(open_set, (f[start], start))

    while open_set:
        priority, curr = heappop(open_set)
        if curr in f and priority == f[curr]:
            if curr == end:
                break
            closed_set.add(curr)

            for nb in nbhd(curr, d_mp):
                if nb not in closed_set:
                    new_dist = g[curr] + nb_dist(curr, nb, d_mp)
                    if nb not in g or new_dist < g[nb]:
                        g[nb] = new_dist
                        f[nb] = new_dist + L1_dist(nb, end) + \
                                        7 * (nb[2] != 't')
                        heappush(open_set, (f[nb], nb))
                
    return g[end]

#=============================

def args():
    return 16807, 48271, 20183

#-----------------------------

def run(depth, target, extend_x, extend_y):
    mp = build_map(depth, target, *args())
    mp[target] = (depth, depth % 3)
    risk = sum(x[1] for x in mp.values())

    mp = extend_map(extend_x, extend_y, mp, depth, *args())
    d_mp = double_map(mp)
    minutes = a_star(d_mp, target)
    
    return risk, minutes

#-----------------------------

def test(extend_x, extend_y):
    print('\ntests:')
    risk, minutes = run(*load('test/22.txt'), extend_x, extend_y)
    print('part 1: passed {} / 1'.format(1 * (risk == 114)))
    print('part 2: passed {} / 1'.format(1 * (minutes == 45)))

#-----------------------------

def main(extend_x, extend_y):
    print('\nmain problem:')
    risk, minutes = run(*load(), extend_x, extend_y)
    print('part 1: risk = {}'.format(risk))
    print('part 2: minutes = {}'.format(minutes))

#=============================

if __name__ == '__main__':

    print('\nproblem 22')
    test(5, 5)
    main(35, 15)
    print()
