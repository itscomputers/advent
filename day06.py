
#   advent/2018/day06.py

from itertools import product

##############################

def parse(data):
    pts = []
    for line in data:
        line.rstrip('\n').replace(' ', '')
        pts.append(tuple(int(x) for x in line.split(',')))
    return pts

##############################

def distance(a, b):
    return sum(abs(pa - pb) for (pa, pb) in zip(a, b))

##############################

def get_grid(pts, buff):
    x = list(map(lambda p : p[0], pts))
    y = list(map(lambda p : p[1], pts))
    x0, x1 = min(x) - buff, max(x) + buff
    y0, y1 = min(y) - buff, max(y) + buff
    grid = list(product(range(x0, x1 + 1), range(y0, y1 + 1)))
    return grid

##############################

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

##############################

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

##############################

def max_region(grid, distances, N):
    return sum(1 for q in grid if distances[q][0][1] < N)

##############################

if __name__ == '__main__':
    
    with open('data/06.txt') as f:
        pts = parse(f.readlines())

    buff = 1
    constraint = 10000
    grid = get_grid(pts, buff)
    distances = resolve(pts, grid)
    area = max_area(grid, distances)
    region = max_region(grid, distances, constraint)

    while True:
        buff *= 2
        grid = get_grid(pts, buff)
        distances = resolve(pts, grid)
        new_region = max_region(grid, distances, constraint)
        if new_region == region:
            break
    
    print(area)
    print(region)


#   Theoretically speaking, if all the points were smashed together,
#   the minimum buffer should be much larger.  Fortunately, the first
#   exercise showed us that the some of the points are somewhat spread
#   out.  I did the lazy thing and checked buffer values until stabilization.
#   P.S. Turns out that buffer=0 is sufficient.
