
#   advent/2018/day25.py

from collections import defaultdict
from itertools import product

#-----------------------------

def parse(data):
    return [tuple(int(x) for x in line.split(',')) for line in data]

#-----------------------------

def load():
    with open('data/25.txt') as f:
        return parse(f.readlines())

#-----------------------------

def test(num):
   datas = [
        ['-1,2,2,0', '0,0,2,-2', '0,0,0,-2', '-1,2,0,0', '-2,-2,-2,2',
         '3,0,2,-1', '-1,3,2,2', '-1,0,-1,0', '0,2,1,-2', '3,0,0,0'],

        ['1,-1,0,1', '2,0,-1,0', '3,2,-1,0', '0,0,3,1', '0,0,-1,-1',
         '2,3,-2,0', '-2,2,0,0', '2,-2,0,-1', '1,-1,0,-1', '3,2,0,2'],

        ['1,-1,-1,-2', '-2,-2,0,1', '0,2,1,3', '-2,3,-2,1', '0,2,3,-2',
         '-1,-1,1,-2', '0,-2,-1,0', '-2,2,3,-1', '1,2,2,0', '-1,-2,0,-2']
    ]
   return parse(datas[num])

#-----------------------------

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

#-----------------------------

def main():
    num_constellations = len(connected_components(build_graph(load())))
    print('number of constellations: {}'.format(num_constellations))

#-----------------------------

if __name__ == '__main__':
    main()
