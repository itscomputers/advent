
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

alphabet = {x : i+1 for i, x in enumerate(string.ascii_uppercase)}

##############################

def process(queue, completed, time_elapsed,
        ready, workers, free_workers, 
        delay, offset):
    while free_workers > 0 and ready != []:
        val = ready.pop(0)
        if delay:
            workers.append([alphabet[val] + offset, val])
        else:
            workers.append([0, val])
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

def order(queue, num_workers=1, delay=False, offset=0):
    completed = ''
    workers = []
    free_workers = num_workers
    time_elapsed = 0
    ready = sorted([x for x in queue if queue[x].parents == []])
    while queue != dict():
        queue, completed, time_elapsed, ready, workers, free_workers = \
                process(queue, completed, time_elapsed,
                        ready, workers, free_workers, 
                        delay, offset)
    return completed, time_elapsed 

#############################

if __name__ == '__main__':

    with open('data/07.txt') as f:
        queue = parse(f.readlines())
    completed, time_elapsed = order(queue)
    print('ordering for single worker, no delay: {}'.format(completed))

    with open('data/07.txt') as f:
        queue = parse(f.readlines())
    completed, time_elapsed = order(queue, num_workers=6, delay=True, offset=60)
    print('ordering for 6 workers, 60sec delay: {}'.format(completed))
    print('time elapsed: {} seconds'.format(time_elapsed))
