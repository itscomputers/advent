
#   advent/2018/day07.py

import re
import string

##############################

alphabet = {x : i+1 for i, x in enumerate(string.ascii_uppercase)}

##############################

class Node:

    def __init__(self, value, delay):
        self.val = value
        self.parents = []
        self.children = []
        self.delay = (delay != 0) *  alphabet[value] + delay

##############################

def parse(data, delay=0):
    nodes = dict()
    parent_pattern = re.compile(r'([A-Z]) must be finished')
    child_pattern = re.compile(r'([A-Z]) can begin')
    for line in data:
        p = parent_pattern.search(line).group(1)
        c = child_pattern.search(line).group(1)
        if p not in nodes:
            nodes[p] = Node(p, delay)
        if c not in nodes:
            nodes[c] = Node(c, delay)
        nodes[p].children.append(c)
        nodes[c].parents.append(p)
    return nodes

##############################

def process(queue, completed, time_elapsed,
        ready, workers, free_workers):
    while free_workers > 0 and ready != []:
        val = ready.pop(0)
        workers.append([queue[val].delay, val])
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
    
    return queue, completed, time_elapsed, ready, workers, free_workers

##############################

def order(queue, num_workers=1, delay=0):
    completed = ''
    workers = []
    free_workers = num_workers
    time_elapsed = 0
    ready = sorted([x for x in queue if queue[x].parents == []])
    while queue != dict():
        queue, completed, time_elapsed, ready, workers, free_workers = \
                process(queue, completed, time_elapsed,
                        ready, workers, free_workers)
    return completed, time_elapsed 

#############################

if __name__ == '__main__':

    with open('data/07.txt') as f:
        queue = parse(f.readlines())
    completed, time_elapsed = order(queue)
    print('{} -- {} seconds'.format(completed, time_elapsed))

    with open('data/07.txt') as f:
        queue = parse(f.readlines(), delay=60)
    completed, time_elapsed = order(queue, num_workers=6, delay=60)
    print('{} -- {} seconds'.format(completed, time_elapsed))
