
#   advent/2018/day10.py

import re

#=============================

def load(filename='data/10.txt'):
    with open(filename) as f:
        return parse(f.readlines())

#-----------------------------

def parse(data):
    pos_pattern = re.compile(r'position=< *(-?\d*), *(-?\d*)>')
    vel_pattern = re.compile(r'velocity=< *(-?\d*), *(-?\d*)>')
    points = []
    for line in data:
        pos = [int(x) for x in pos_pattern.search(line).group(1, 2)]
        vel = [int(x) for x in vel_pattern.search(line).group(1, 2)]
        points.append(Point(pos, vel))
    return points

#=============================

class Point:

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

#=============================

def positions(pts, t):
    return list(map(lambda p: [x + t*y for x, y in zip(p.pos, p.vel)], pts))

#-----------------------------

def boundary(pts, t):
    pos = positions(pts, t)
    x0, x1 = min(p[0] for p in pos), max(p[0] for p in pos)
    y0, y1 = min(p[1] for p in pos), max(p[1] for p in pos)
    return (x0, y0), (x1, y1)

#-----------------------------

def area(pts, t):
    (x0, y0), (x1, y1) = boundary(pts, t)
    return (x1 - x0) * (y1 - y0)

#-----------------------------

def time(pts):
    a = area(pts, 0)
    index = 0
    while True:
        index += 1
        new_a = area(pts, index)
        if new_a <= a:
            a = new_a
        else:
            break
    return index - 1

#-----------------------------

def plot(pts, t):
    pos = positions(pts, t)
    (x0, y0), (x1, y1) = boundary(pts, t)
    for j in range(y0, y1+1):
        for i in range(x0, x1+1):
            if [i,j] in pos:
                print('#', end='')
            else:
                print('.', end='')
        print()

#=============================

def test():
    print('\ntests:')
    pts = load('test/10.txt')
    time_elapsed = time(pts)
    print('part 1:')
    plot(pts, time_elapsed)
    print('part 2: passed {} / 1'.format(1 * (time_elapsed == 3)))

#-----------------------------

def main():
    print('\nmain problem:')
    pts = load()
    time_elapsed = time(pts)
    print('part 1:')
    plot(pts, time_elapsed)
    print('part 2: time_elapsed = {}'.format(time_elapsed))

#=============================

if __name__ == '__main__':

    print('\nproblem 10')
    test()
    main()
    print()
