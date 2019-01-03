
#   advent/2018/day18.py

from itertools import product
from collections import Counter, defaultdict

#=============================

def load(filename='data/18.txt'):
    with open(filename) as f:
        return parse([x.strip() for x in f.readlines()])

#-----------------------------

def parse(data):
    resources = dict()
    for y, line in enumerate(data):
        for x, ch in enumerate(line):
            resources[(x,y)] = ch
    return resources

#=============================

class Area:

    def __init__(self, resources):
        self.resources = resources
        self.cycle = ['.', '|', '#', '.']
        self.xmax = max(p[0] for p in resources.keys()) + 1
        self.ymax = max(p[1] for p in resources.keys()) + 1

    #-------------------------

    def __repr__(self):
        return '\n'.join(
            ''.join(
                self.resources[(x,y)] for x in range(self.xmax)
            ) for y in range(self.ymax)
        )

    #-------------------------

    def nbhd(self, point):
        x, y = point
        return [self.resources[(r, s)] for (r, s)\
                in product(range(x-1, x+2), range(y-1, y+2)) \
                if 0 <= r < self.xmax \
                and 0 <= s < self.ymax \
                and (r, s) != (x, y)]

    #-------------------------

    def scan(self, point):
        n = self.nbhd(point)
        if self.resources[point] == '.':
            return n.count('|') > 2
        if self.resources[point] == '|':
            return n.count('#') > 2
        if self.resources[point] == '#':
            return (n.count('#') * n.count('|')) == 0

    #-------------------------

    def eval(self, point):
        for i in range(3):
            if self.resources[point] == self.cycle[i] and self.scan(point):
                return self.cycle[i+1]
        return self.resources[point]

    #-------------------------

    def advance(self):
        new_resources = {point : self.eval(point) for point in self.resources}
        self.resources = new_resources

    #-------------------------

    def status(self):
        return Counter(self.resources.values())

    #-------------------------

    def value(self):
        return self.status()['|'] * self.status()['#']

#=============================

def find_repeat(area):
    resources = []
    for i in range(1000):
        if area.resources in resources:
            return resources.index(area.resources), i
        resources.append(area.resources)
        area.advance()

#=============================

def part1(data):
    area = Area(data)
    for i in range(10):
        area.advance()
    return area.value()
    
#-----------------------------

def part2(data):
    area = Area(data)
    i0, i1 = find_repeat(area)
    for j in range((10**9 - i1) % (i1 - i0)):
        area.advance()
    return area.value()

#-----------------------------

def test():
    print('\ntests:')
    value = part1(load('test/18.txt'))
    print('part 1: passed {} / 1'.format(1 * (value == 1147)))

#-----------------------------

def main():
    print('\nmain problem:')
    print('part 1: value = {}'.format(part1(load())))
    print('part 2: value = {}'.format(part2(load())))

#=============================

if __name__ == '__main__':

    print('\nproblem 18')
    test()
    main()
    print()
