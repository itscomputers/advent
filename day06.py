
#   advent/2018/day06.py

import re
from itertools import product

#=============================

def load(filename='data/06.txt'):
    with open(filename) as f:
        return parse(f.readlines())

#-----------------------------

def parse(data):
    point_pattern = re.compile(r'(\d+), (\d+)')
    pts = []
    for line in data:
        if point_pattern.search(line) is not None:
            pts.append(tuple(int(x) for x in \
                    point_pattern.search(line).group(1,2)))
    return pts

#=============================

def distance(pt1, pt2):
    return sum(map(lambda x, y: abs(x - y), pt1, pt2))

#-----------------------------

def get_grid(pts, buff):
    x = list(map(lambda p : p[0], pts))
    y = list(map(lambda p : p[1], pts))
    x0, x1 = min(x) - buff, max(x) + buff
    y0, y1 = min(y) - buff, max(y) + buff
    grid = list(product(range(x0, x1 + 1), range(y0, y1 + 1)))
    return grid

#-----------------------------

def resolve(pts, grid):
    distances = {q : ((distance(q, pts[0]), )*2, [pts[0]]) for q in grid}
    for p in pts[1:]:
        for q in grid:
            new_dist = distance(p, q)
            (dist, dist_sum), closest_points = distances[q]
            dist_sum += new_dist
            if dist == new_dist:
                closest_points.append(p)
                distances[q] = ((dist, dist_sum), closest_points)
            elif dist > new_dist:
                distances[q] = ((new_dist, dist_sum), [p])
            else:
                distances[q] = ((dist, dist_sum), closest_points)
    return distances

#-----------------------------

def max_area(grid, distances):
    (x0, y0) = grid[0]
    (x1, y1) = grid[-1]
    areas = dict()
    for q in grid:
        closest_points = distances[q][1]
        if len(closest_points) == 1:
            closest = closest_points[0]
            if q[0] in [x0, x1] or q[1] in [y0, y1]:
                areas[closest] = 0
            else:
                if closest not in areas:
                    areas[closest] = 1
                elif areas[closest] > 0:
                    areas[closest] += 1
    return max(areas.values())

#-----------------------------

def max_region(grid, distances, N):
    return sum(1 for q in grid if distances[q][0][1] < N)

#-----------------------------

def stabilize_region(pts, constraint):
    buff = 1
    grid = get_grid(pts, buff)
    region = max_region(grid, resolve(pts, grid), constraint)
    while True:
        buff *= 2
        grid = get_grid(pts, buff)
        new_region = max_region(grid, resolve(pts, grid), constraint)
        if new_region == region:
            break
    return region

#=============================

def test():
    pts = load('test/06.txt')
    grid = get_grid(pts, 0)
    area = max_area(grid, resolve(pts, grid))
    region = stabilize_region(pts, 32)
    return (area == 17), (region == 16)
    
#-----------------------------

def main():
    pts = load()
    grid = get_grid(pts, 0)
    area = max_area(grid, resolve(pts, grid))
    region = stabilize_region(pts, 10000)
    print('\nmain problem:')
    print('part 1: largest area = {}'.format(area))
    print('part 2: largest area = {}'.format(region))

#=============================

if __name__ == '__main__':
    test_one, test_two = test()
    print('part 1 tests: passed {} / 1'.format(1 * test_one))
    print('part 2 tests: passed {} / 1'.format(1 * test_two))
    
    main()

#=============================
#   Theoretically speaking, if all the points were smashed together,
#   the minimum buffer should be much larger.  Fortunately, the first
#   exercise showed us that the some of the points are somewhat spread
#   out.  I did the lazy thing and checked buffer values until stabilization.
#   P.S. Turns out that buffer=0 is sufficient.
