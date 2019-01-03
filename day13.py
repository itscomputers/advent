
#   advent/2018/day13.py

#=============================

def load(filename='data/13.txt'):
    with open(filename) as f:
        return parse(f.readlines())

#-----------------------------

def parse(data):
    nodes = dict()
    carts = dict()
    for y, line in enumerate(data):
        line = line.rstrip().rstrip('n')
        for x, ch in enumerate(line):
            if ch not in ['-', '|', ' ']:
                if ch == 'v':
                    carts[(x,y)] = (0,1)
                elif ch == '^':
                    carts[(x,y)] = (0,-1)
                elif ch == '>':
                    carts[(x,y)] = (1,0)
                elif ch == '<':
                    carts[(x,y)] = (-1,0)
                else:
                    nodes[(x,y)] = ch
    return Queue([Cart(k, v) for k, v in carts.items()], nodes)

#=============================

class Cart:

    def __init__(self, pos, direction):
        self.pos = pos
        self.dir = direction
        self.turn_count = 0

    #-------------------------

    def turn(self, ch):
        if ch == '/':
            self.dir = (-self.dir[1], -self.dir[0])
        elif ch == '\\':
            self.dir = (self.dir[1], self.dir[0])
        elif ch == '+':
            if self.turn_count == 0:
                dirs = [(1,0), (0,1), (-1,0), (0,-1)]
                self.dir = dirs[dirs.index(self.dir) - 1]
            elif self.turn_count == 2:
                dirs = [(1,0), (0,-1), (-1,0), (0,1)]
                self.dir = dirs[dirs.index(self.dir) - 1]
            self.turn_count += 1
            self.turn_count %= 3

    #-------------------------

    def advance(self):
        self.pos = tuple(s + t for s, t in zip(self.pos, self.dir))

#=============================

class Queue:

    def __init__(self, carts, nodes):
        self.carts = carts
        self.nodes = nodes
        self.sort()
        self.collisions = []

    #-------------------------

    def __repr__(self):
        return '\n'.join(
            '{} -->{}'.format(cart.pos, cart.dir) \
                    for cart in self.carts)

    #-------------------------

    def sort(self):
        self.carts.sort(key=lambda c: (c.pos[1], c.pos[0]))

    #-------------------------

    def advance(self):
        for cart in self.carts:
            cart.advance()
            positions = [c.pos for c in self.carts]
            if positions.count(cart.pos) > 1:
                self.collisions.append(cart.pos)
                self.carts = [c for c in self.carts if c.pos != cart.pos]
            if cart.pos in self.nodes:
                cart.turn(self.nodes[cart.pos])
        self.sort()

#=============================

def run(queue):
    while len(queue.carts) > 1:
        queue.advance()
    return queue.collisions, queue.carts

#-----------------------------

def test():
    print('\ntests:')
    part1 = run(load('test/13-a.txt'))[0][0]
    print('part 1: passed {} / 1'.format(1 * (part1 == (7, 3))))
    part2 = run(load('test/13-b.txt'))[1][0].pos
    print('part 2: passed {} / 1'.format(1 * (part2 == (6, 4))))
    
#-----------------------------

def main():
    print('\nmain problem:')
    part1, part2 = run(load())
    print('part 1: first collision = {},{}'.format(*part1[0]))
    print('part 2: final cart = {},{}'.format(*part2[0].pos))

#=============================

if __name__ == '__main__':

    print('\nproblem 13')
    test()
    main()
    print()
