
#   advent/2018/day12.py

import re

#=============================

def load(filename='data/12.txt'):
    with open(filename) as f:
        return parse(f.readlines())

#-----------------------------

def convert(string):
    return re.sub('\.', '0', re.sub('#', '1', string))

#-----------------------------

def parse(data):
    state_pattern = re.compile('initial state: ([#\.]*)\\n')
    evol_pattern = re.compile('([#\.]{5}) => ([#\.])\\n')
    state = set(i for i, ch in \
            enumerate(state_pattern.search(data[0]).group(1)) \
            if ch == '#')
    signatures = set(int(convert(p), 2) \
            for (p, e) in [evol_pattern.search(line).group(1,2) \
            for line in data[1:] if evol_pattern.search(line)] \
            if e == '#')
    return state, signatures

#=============================

def surrounding(state, index):
    return sum( 2**(2 + index - i) * (i in state) \
                for i in range(index - 2, index + 3))

#-----------------------------

def evolve(state, signatures):
    return set(index for index in \
            range(min(state)-5, max(state)+5) \
            if surrounding(state, index) in signatures)

#-----------------------------

def print_state(state, x0, x1):
    print(''.join('#'*(i in state) + '.'*(i not in state) \
            for i in range(x0, x1)))

#-----------------------------

def find_stabilization(state, signatures, threshold):
    sums = [sum(state)]
    steps = []
    
    for i in range(threshold):
        state = evolve(state, signatures)
        sums.append(sum(state))
        steps.append(sums[-1] - sums[-2])
    
    while steps[-threshold:] != [steps[-1]] * threshold:
        i += 1
        state = evolve(state, signatures)
        sums.append(sum(state))
        steps.append(sums[-1] - sums[-2])
    
    return i + 1, steps[-1], sums[-1]

#=============================

def test():
    print('\ntests:')
    state, signatures = load('test/12.txt')
    for i in range(20):
        state = evolve(state, signatures)
    print('part 1: passed {} / 1'.format(1 * (sum(state) == 325)))

#-----------------------------

def main():
    print('\nmain problem:')
    state, signatures = load()
    for i in range(20):
        state = evolve(state, signatures)
    print('part 1: sum = {}'.format(sum(state)))
    state, signatures = load()
    index, step, offset = find_stabilization(state, signatures, 20)
    print('part 2: sum = {}'.format((50*10**9 - index) * step + offset))

#=============================

if __name__ == '__main__':

    print('\nproblem 12')
    test()
    main()
    print()
