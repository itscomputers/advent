
#   advent/2018/day11.py

from itertools import product

##############################

def power(ser, x, y):
    "ser: serial number | x, y: coordinates"
    return ((pow(x + 10, 2, 1000) * y + (x + 10) * ser) % 1000 // 100) - 5

##############################

def grid(ser):
    "s: serial number"
    return {t : power(ser, *t) for t in product(range(1,301), range(1, 301))}

##############################

def subgrid(g, d, x, y, PRINT=False):
    s = 0
    for j in range(y, y+d):
        for i in range(x, x+d):
            if PRINT:   print(g[i,j], end= '  ')
            s += g[i,j]
        if PRINT:   print()
    return s

##############################

def max_power_by_size(g, d):
    return max([[(x, y), subgrid(g, d, x, y, False)] \
            for (x, y) in product(range(1, 302-d), range(1, 302-d))],
            key = lambda x: x[1])

##############################

def max_power(g):
    pos, total = max_power_by_size(g, 1)
    dim = 1
    for d in range(1, 300):
        new_pos, new_total = max_power_by_size(g, d+1)
        if new_total >= total:
            pos = new_pos
            total = new_total
            dim = d
        else:
            break
    return pos, d, total

##############################

if __name__ == '__main__':

    with open('data/11.txt') as f:
        ser = int(f.read()) % 1000

    g = grid(ser)

    pos, total = max_power_by_size(g, 3)
    print('{},{}'.format(*pos))

    pos, dim, total = max_power(g)
    print('{},{},{}'.format(*pos, dim))
