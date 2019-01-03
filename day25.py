
#   advent/2018/day25.py

from collections import defaultdict
from itertools import product

#=============================

def load(filename='data/25.txt'):
    with open(filename) as f:
        return parse(f.readlines())

#-----------------------------

def parse(data):
    return [tuple(int(x) for x in line.split(',')) for line in data]

#=============================

def dist(pt1, pt2):
    return sum(map(lambda x, y: abs(x - y), pt1, pt2))

#-----------------------------

def build_graph(points):
    graph = defaultdict(set)
    for pt1, pt2 in product(points, points):
        if pt1 <= pt2 and dist(pt1, pt2) < 4:
            graph[pt1].add(pt2)
            graph[pt2].add(pt1)
    return graph

#-----------------------------

def connected_components(graph):
    visited = set()
    
    def component(pt):
        comp = set()
        queue = set([pt])
        while queue != set():
            pt = queue.pop()
            visited.add(pt)
            queue |= (graph[pt] - visited)
            comp.add(pt)
        return comp

    components = []
    for pt in graph:
        if pt not in visited:
            components.append(component(pt))

    return components

#=============================

def run(data):
    graph = build_graph(data)
    components = connected_components(graph)
    return len(components)

#-----------------------------

def test():
    print('\ntests:')
    components = [run(load('test/25-{}.txt'.format(ch))) for ch in 'abc']
    answers = [4, 3, 8]
    print('part 1: passed {} / {}'.format(
        sum(map(lambda x, y: x == y, components, answers)),
        len('abc')))

#-----------------------------

def main():
    print('\nmain problem:')
    components = run(load())
    print('part 1: number of constellations = {}'.format(components))

#-----------------------------

if __name__ == '__main__':

    print('\nproblem 25')
    test()
    main()
    print()
