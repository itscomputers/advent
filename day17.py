
#   advent/2018/day17.py

import re
from functools import reduce

##############################

def parse(data):
    clay = set()
    h_pattern = re.compile(r'x=(\d+), y=(\d+)..(\d+)')
    v_pattern = re.compile(r'y=(\d+), x=(\d+)..(\d+)')
    for line in data:
        if h_pattern.search(line) is not None:
            x, y0, y1 = [int(t) for t in h_pattern.search(line).group(1,2,3)]
            for y in range(y0, y1+1):
                clay.add((x,y))
        elif v_pattern.search(line) is not None:
            y, x0, x1 = [int(t) for t in v_pattern.search(line).group(1,2,3)]
            for x in range(x0, x1+1):
                clay.add((x,y))
    return clay

##############################

class Reservoir:

    def __init__(self, clay):
        self.clay = clay
        self.stationary = set()
        self.flowing = set() 
        X = [x for (x,y) in self.clay] + [500]
        Y = [y for (x,y) in self.clay]
        self.xmin, self.xmax = min(X) - 1, max(X) + 1
        self.ymin, self.ymax = min(Y), max(Y)
        self.sources = [(500, self.ymin)]

    ##########################

    def __repr__(self):
        lines = ['.' * (500 - self.xmin) + '+' + '.' * (self.xmax - 500), '']
        for y in range(self.ymin, self.ymax + 1):
            line = ''
            for x in range(self.xmin, self.xmax + 1):
                if (x,y) in self.clay:
                    line += '#'
                elif (x,y) in self.stationary:
                    line += '~'
                elif (x,y) in self.flowing:
                    line += '|'
                else:
                    line += '.'
            lines.append(line)
        return '\n'.join(lines)

    ##########################

    def clay_below(self, p):
        "p: source point -> q: point above clay"
        possible = [(x, y) for (x, y) in self.clay if y > p[1] and x == p[0]]
        if possible == []:
            return None
        else:
            (x, y) = min(possible)
            return (x, y-1)

    ##########################

    def base(self, p):
        "p: point above clay -> x0, x1: left/right x-coords of base"
        x, y = p
        x0, x1 = x, x
        while (x0-1, y+1) in (self.clay | self.stationary):
            x0 -= 1
        while (x1+1, y+1) in (self.clay | self.stationary):
            x1 += 1
        return x0, x1

    ##########################

    def walls(self, p, x_base):
        "p: point above clay, x0, x1: base(p) -> left, right: walls"
        x, y = p
        x0, x1 = x_base
        possible = [s for (s, t) in self.clay if t == y and x0 <= s <= x1]
        
        try:
            left = max(s for s in possible if s < x)
        except ValueError:
            left = None
        try:
            right = min(s for s in possible if s > x)
        except ValueError:
            right = None

        return left, right

    ##########################

    def h_fill(self, p):
        "p: point above clay -> None, update flowing, stationary"
        x0, x1 = self.base(p)
        left, right = self.walls(p, (x0, x1))
        if left is None and right is None:
            self.flowing |= set((x, p[1]) for x in range(x0, x1 + 1))
            self.sources += [q for q in [(x0 - 1, p[1]), (x1 + 1, p[1])] \
                                if q not in self.sources]
        elif left is None:
            self.flowing |= set((x, p[1]) for x in range(x0, right))
            self.sources += [q for q in [(x0 - 1, p[1])] \
                                if q not in self.sources]
        elif right is None:
            self.flowing |= set((x, p[1]) for x in range(left + 1, x1 + 1))
            self.sources += [q for q in [(x1 + 1, p[1])] \
                                if q not in self.sources]
        else:
            self.stationary |= set((x, p[1]) for x in range(left + 1, right))

    ##########################

    def well_fill(self, p):
        "p: source point -> None, update flowing, stationary, sources"
        q = self.clay_below(p)
        if q is None:
            self.flowing |= set((p[0], y) for y in range(p[1], self.ymax + 1))
        else:
            self.flowing |= set((p[0], y) for y in range(p[1], q[1]))
            x, y = q
            while (x, y+1) in (self.clay | self.stationary):
                self.h_fill((x, y))
                y -= 1
                
    ##########################

    def fill(self):
        while self.sources != []:
            source = self.sources.pop(0)
            self.well_fill(source)
            
##############################

if __name__ == '__main__':

    with open('data/17.txt') as f:
        res = Reservoir(parse(f.readlines()))

    res.fill()

    print(len(res.flowing | res.stationary))
    print(len(res.stationary))
