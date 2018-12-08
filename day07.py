
#   advent/2018/day07.py

import re
import string

##############################

class Node:

    def __init__(self, value):
        self.val = value
        self.parents = []
        self.children = []

##############################

def parse(data):
    nodes = dict()
    parent_pattern = re.compile(r'[A-Z] must be finished')
    child_pattern = re.compile(r'[A-Z] can begin')
    for line in data:
        p = parent_pattern.search(line).group().split(' ')[0]
        c = child_pattern.search(line).group().split(' ')[0]
        if p not in nodes:
            nodes[p] = Node(p)
        if c not in nodes:
            nodes[c] = Node(c)
        nodes[p].children.append(c)
        nodes[c].parents.append(p)
    return nodes

##############################

alphabet_delay = {x : i+1 for i, x in enumerate(string.ascii_uppercase)}

def delay(val, offset):
    return alphabet_delay[val] + offset

##############################

def process(queue, ready, completed,
        workers, free_workers, offset, time_elapsed):
    while free_workers > 0 and ready != []:
        val = ready.pop(0)
        workers.append([delay(val, offset), val])
        free_workers -= 1
    workers.sort()

    time, val = workers.pop(0)
    for w in workers:
        w[0] -= time
    completed += val
    time_elapsed += time
    free_workers += 1

    for c_val in queue[val].children:
        queue[c_val].parents.remove(val)
        if queue[c_val].parents == []:
            ready.append(c_val)
        ready.sort()
    del queue[val]
    
    return queue, ready, completed, workers, free_workers, time_elapsed

##############################

def order(tree, num_workers, offset):
    queue = tree
    completed = ''
    workers = []
    free_workers = num_workers
    time_elapsed = 0
    ready = sorted([x for x in queue if queue[x].parents == []])
    while queue != dict():
        queue, ready, completed, workers, free_workers, time_elapsed = \
                process(queue, ready, completed, 
                        workers, free_workers, offset, time_elapsed)
    return time_elapsed 

#############################

if __name__ == '__main__':

    with open('data/07.txt') as f:
        tree = parse(f.readlines())

    print(order(tree, 6, 60))
