
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

def run(data):
    part1 = metadata_sum([x for x in data], problem=1)
    part2 = metadata_sum(data, problem=2)
    return part1, part2

#-----------------------------

def test():
    print('\ntests:')
    part1, part2 = run(load('test/08.txt'))
    print('part 1: passed {} / 1'.format(1 * (part1 == 138)))
    print('part 2: passed {} / 2'.format(1 * (part2 == 66)))

#-----------------------------

def main():
    print('\nmain problem:')
    part1, part2 = run(load())
    print('part 1: metadata sum = {}'.format(part1))
    print('part 2: metadata sum = {}'.format(part2))

##############################

if __name__ == '__main__':

    print('\nproblem 8')
    test()
    main()
    print()
