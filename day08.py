
#   advent/2018/day08.py

#=============================

def load(filename='data/08.txt'):
    with open(filename) as f:
        return [int(x) for x in f.read().split(' ')]

#=============================

def node_sum(data, problem):
    [c, m, *data] = data
    if c == 0:
        return data[m:], sum(data[:m])

    sums = []
    for i in range(c):
        data, meta_sum = node_sum(data, problem)
        sums.append(meta_sum)
    
    if problem == 1:
        return data[m:], sum(sums) + sum(data[:m])
    else:
        return data[m:], sum(sums[i-1] for i in data[:m] if i <= c)

#-----------------------------

def metadata_sum(data, problem=1):
    sums = []
    while data != []:
        data, meta_sum = node_sum(data, problem)
        sums.append(meta_sum)
    if problem == 1:
        return sum(sums)
    else:
        return sums[0]

#=============================

def test():
    data = load('test/08.txt')
    return metadata_sum([x for x in data]) == 138, \
            metadata_sum(data, problem=2) == 66

#-----------------------------

def main():
    data = load()
    print('\nmain problem:')
    print('part 1: metadata sum = {}'.format(metadata_sum([x for x in data])))
    print('part 2: metadata sum = {}'.format(metadata_sum(data, problem=2)))

##############################

if __name__ == '__main__':
    test_one, test_two = test()
    print('part 1 tests: passed {} / 1'.format(1 * test_one))
    print('part 2 tests: passed {} / 1'.format(1 * test_two))
    
    main()
