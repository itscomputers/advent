
import re
from functools import reduce
from itertools import product
from collections import defaultdict
from random import sample

#-----------------------------

def parse(data):
    points = dict()
    point_pattern = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>')
    radius_pattern = re.compile(r'r=(\d+)')
    for line in data:
        if point_pattern.search(line) is not None:
            point = tuple(map(lambda x: int(x), 
                    point_pattern.search(line).group(1,2,3)))
        if radius_pattern.search(line) is not None:
            radius = int(radius_pattern.search(line).group(1))
        points[point] = radius
    return points

#-----------------------------

def load():
    with open('data/23.txt') as f:
        return parse([x.rstrip() for x in f.readlines()])

#-----------------------------

def dist(pt1, pt2):
    return sum(map(lambda t: abs(t[0] - t[1]), zip(pt1, pt2)))

#-----------------------------

def pts_nbhd(pt, points):
    return [nb for nb in points if dist(pt, nb) <= points[pt]]

#-----------------------------

def bots_in_range(pt, points):
    return len([nb for nb in points if dist(pt, nb) <= points[nb]])

#-----------------------------

def intersect(pt1, pt2, points):
    return dist(pt1, pt2) <= points[pt1] + points[pt2]

#-----------------------------

def build_graph(points):
    graph = defaultdict(set)
    for pt1, pt2 in product(points.keys(), points.keys()):
        if pt1 < pt2 and intersect(pt1, pt2, points):
            graph[pt1].add(pt2)
            graph[pt2].add(pt1)
    return graph

#-----------------------------

def bron_kerbosch(R, P, X, graph):
    if (P | X) == set():
        yield R
    for v in P.copy():
        for r in bron_kerbosch(R | set([v]), P & graph[v], X & graph[v], graph):
            yield r
        P.remove(v)
        X.add(v)

#-----------------------------

def dot_product(pt1, pt2):
    return sum(map(lambda x, y: x * y, pt1, pt2))

#-----------------------------

def inverse(pt):
    return [dot_product(vec, pt) for vec in \
            [(0, .5, .5), (.5, 0, -.5), (.5, -.5, 0)]]

#-----------------------------

def intersection(clique, points):
    vals = [[
        max(dot_product(pt, vec) - points[pt] for pt in clique),
        min(dot_product(pt, vec) + points[pt] for pt in clique)
        ] for vec in [(1,1,1),(1,1,-1), (1,-1,1)]]
    signatures = [
            [(0,0), (1,0), (2,0)], 
            [(0,1), (1,1), (2,1)],
            [(0,0), (1,1), (2,0)],
            [(0,1), (1,0), (2,1)],
            [(0,0), (1,0), (2,1)],
            [(0,1), (1,1), (2,0)]]
    vecs = [[vals[i][j] for (i, j) in sig] for sig in signatures]
    return [inverse(vec) for vec in vecs]

#-----------------------------

def main():
    pts = load()
    strongest = max(pts, key=pts.get)
    num_bots = len(pts_nbhd(strongest, pts))

    print('strongest point: {}\nwith radius: {}\nand {} bots in radius'\
            .format(strongest, pts[strongest], num_bots))

    graph = build_graph(pts)
    g = bron_kerbosch(set(), set(graph.keys()), set(), graph)
    clique = list(next(g))
    octahedron = intersection(clique, pts)
    closest_distance = int(min(sum(pt) for pt in octahedron))
    
    print('closest point within range of most bots: {}'.format(closest_distance))

#-----------------------------

if __name__ == '__main__':

    main()
