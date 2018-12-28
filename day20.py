
#   advent/2018/day20.py

import re
from itertools import product

##############################

class Node:

    def __init__(self, word):
        self.word = word
        self.children = []
        self.loop = None

    def __repr__(self):
        return self.word + \
                (self.children != []) * ' -> {}'.format(self.children)

##############################

class Map:

    def __init__(self, string):
        self.string = string
        self.pattern = re.compile(r'^[NESW]+')
        self.loop_pattern = re.compile(r'^\([NESW]+\|\)')
        self.tokens = self.tokenize(string)
        self.base = Node(next(self.tokens))
        self.curr = self.base
        self.open = []
        self.populate()
        self.build_map()
        self.compute_distances()

    def __repr__(self):
        return format(self.base)

    ##########################

    def tokenize(self, string):
        while string != '$':
            if self.loop_pattern.search(string) is not None:
                loop = self.loop_pattern.search(string).group()
                string = string.split(loop, 1)[-1]
                yield loop
            elif self.pattern.search(string) is not None:
                word = self.pattern.search(string).group()
                string = string.split(word, 1)[-1]
                yield word
            else:
                if string[0] in ['(', '|', ')']:
                    yield string[0]
                string = string[1:]

    ##########################

    def populate(self):
        while True:
            try:
                t = next(self.tokens)
                if t == '(':
                    self.open.append(self.curr)
                elif t == '|':
                    self.curr = self.open[-1]
                elif t == ')':
                    self.open.pop()
                elif self.loop_pattern.search(t) is not None:
                    self.curr.loop = self.pattern.search(t[1:]).group()
                elif self.pattern.search(t) is not None:
                    node = Node(t)
                    self.curr.children.append(node)
                    self.curr = node
            except StopIteration:
                break

    ##########################

    def move(self, loc, ch):
        if ch == 'N':
            return (loc[0], loc[1] + 1), (loc[0], loc[1] + 2)
        if ch == 'E':
            return (loc[0] + 1, loc[1]), (loc[0] + 2, loc[1])
        if ch == 'S':
            return (loc[0], loc[1] - 1), (loc[0], loc[1] - 2)
        if ch == 'W':
            return (loc[0] - 1, loc[1]), (loc[0] - 2, loc[1])

    ##########################

    def build_map(self):
        visited = set([(0, 0)])
        doors = set()
        queue = [(self.base, (0, 0))]
        while queue != []:
            node, loc = queue.pop()
            for ch in node.word:
                door, loc = self.move(loc, ch)
                visited.add(loc)
                doors.add(door)
            if node.loop is not None:
                for ch in node.loop:
                    door, loc = self.move(loc, ch)
                    visited.add(loc)
                    doors.add(door)
            for child in node.children:
                queue.append((child, loc))
        self.visited = visited
        self.doors = doors

    ##########################

    def nbhd(self, loc):
        nbhd = []
        if (loc[0], loc[1] + 1) in self.doors:
            nbhd.append((loc[0], loc[1] + 2))
        if (loc[0], loc[1] - 1) in self.doors:
            nbhd.append((loc[0], loc[1] - 2))
        if (loc[0] + 1, loc[1]) in self.doors:
            nbhd.append((loc[0] + 2, loc[1]))
        if (loc[0] - 1, loc[1]) in self.doors:
            nbhd.append((loc[0] - 2, loc[1]))
        return nbhd

    ##########################

    def compute_distances(self):
        visited = []
        distances = dict()
        queue = [((0, 0), 0)]
        while queue != []:
            loc, dist = queue.pop()
            for nb in self.nbhd(loc):
                if nb not in visited:
                    queue.append((nb, dist + 1))
            visited.append(loc)
            distances[loc] = dist
        self.distances = distances

##############################

if __name__ == '__main__':

    with open('data/20.txt') as f:
        m = Map(f.read().rstrip())

    print(max(m.distances.values()))
    print(len([loc for loc, dist in m.distances.items() if dist > 999]))
