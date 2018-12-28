
#   advent/2018/day22.py

import re
from functools import reduce
from itertools import product

#-----------------------------

def parse(data):
    for line in data:
        if re.search(r'depth: (\d+)', line):
            depth = int(re.search(r'depth: (\d+)', line).group(1))
        if re.search(r'target: (\d+),(\d+)', line):
            target = tuple(map(lambda x: int(x),
                re.search(r'target: (\d+),(\d+)', line).group(1,2)))
    return depth, target

#-----------------------------

def load():
    with open('data/22.txt') as f:
        return parse([x.rstrip() for x in f.readlines()])

#-----------------------------

def main(depth, target):
    mul_x = 16807
    mul_y = 48271
    mod = 20183
    mp = build_map(depth, target, mul_x, mul_y, mod)
    mp[target] = (depth, depth % 3)

    risk = sum(x[1] for x in mp.values())
    print('risk: {}'.format(risk))

    mp = extend_map(50, 50, mp, depth, mul_x, mul_y, mod)
    d_mp = double_map(mp)
    
    print('shortest path to target: {}'.format(a_star(d_mp, target)))

#-----------------------------

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

def nb_dist(pt, nb):
    if pt[:2] == nb[:2]:
        return 7
    elif pt[2] == nb[2]:
        return 1

#-----------------------------

def L1_dist(pt, nb):
    return sum(map(lambda t: abs(t[1] - t[0]), zip(pt[:2], nb[:2])))

#-----------------------------

def nbhd(pt, d_mp):
    x, y, z = pt
    return [nb for nb in d_mp \
            if nb in [(x, y-1, z), (x, y+1, z), (x-1, y, z), (x+1, y, z)] \
            or nb[:2] == (x, y)]

#-----------------------------

def a_star(d_mp, target):
    start = (0, 0, 't')
    end = (*target, 't')

    open_set = set([start])
    closed_set = set()

    g_score = {start : 0}
    f_score = {start : L1_dist(start, end)}
    
    while open_set != set() and end not in closed_set:
        curr = min((pt for pt in open_set if pt in f_score), key=f_score.get)
        open_set.remove(curr)
        closed_set.add(curr)

        for nb in nbhd(curr, d_mp):
            if nb not in closed_set:
                dist = g_score[curr]
                n_dist = nb_dist(curr, nb)
                
                if nb not in open_set:
                    open_set.add(nb)
                
                if nb not in g_score or g_score[nb] > dist + n_dist:
                    g_score[nb] = dist + n_dist
                    f_score[nb] = g_score[nb] + L1_dist(nb, end)

    return g_score[end]

##############################

if __name__ == '__main__':

    main(*load())
