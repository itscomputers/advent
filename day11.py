
#   advent/2018/day11.py

from itertools import product

#=============================

def load(filename='data/11.txt'):
    with open(filename) as f:
        return int(f.read()) % 1000

#=============================

def power(ser, x, y):
    "ser: serial number | x, y: coordinates"
    return ((pow(x + 10, 2, 1000) * y + (x + 10) * ser) % 1000 // 100) - 5

#-----------------------------

def grid(ser):
    "ser: serial number"
    return {t : power(ser, *t) for t in product(range(1,301), range(1, 301))}

#-----------------------------

def restrict(g, d, x, y):
    "g: grid"
    return {(i, j) : g[i, j] \
            for (i, j) in product(range(x, x+d), range(y, y+d))}

#-----------------------------

def vert_sums(g):
    prefix = {x : [0] for x in range(1, 301)}
    for x in prefix:
        for y in range(1, 301):
            prefix[x].append(prefix[x][-1] + g[x, y])
    return prefix

#-----------------------------

def max_subarray(arr, size):
    curr_sum = sum(arr[:size])
    max_sum = curr_sum
    max_index = 0
    for i, x in enumerate(arr[size:]):
        first = arr[i]
        curr_sum = curr_sum - first + x
        if curr_sum > max_sum:
            max_sum = curr_sum
            max_index = i + 1
    return max_index, max_sum

#-----------------------------

def squares_by_size(g, prefix):
    squares = dict()
    for size in range(1, 300):
        for y in range(1, 301 - size):
            arr = [prefix[x][y+size-1] - prefix[x][y-1] for x in range(1, 301)]
            max_index, max_sum = max_subarray(arr, size)
            squares[(max_index + 1, y, size)] = max_sum
    return squares

#-----------------------------

def max_square_by_size(g, size, squares):
    squares = {k : v for k, v in squares.items() if k[2] == size}
    k = max(squares, key=squares.get)
    return (*k, squares[k])

#-----------------------------

def max_square(g, squares):
    k = max(squares, key=squares.get)
    return (*k, squares[k])

#=============================

def run(data):
    g = grid(data)
    squares = squares_by_size(g, vert_sums(g))
    x, y, size, power = max_square_by_size(g, 3, squares)
    part1 = (x, y)
    x, y, size, power = max_square(g, squares)
    part2 = (x, y, size)
    return part1, part2

#-----------------------------

def test():
    print('\ntests:')
    results = [run(load('test/11-{}.txt'.format(ch))) for ch in 'ab']
    answers = [((33, 45), (90, 269, 16)), ((21, 61), (232, 251, 12))]
    print('part 1: passed {} / {}'.format(
        sum(map(lambda x, y: 1 * (x[0] == y[0]), results, answers)), 2))
    print('part 2: passed {} / {}'.format(
        sum(map(lambda x, y: 1 * (x[1] == y[1]), results, answers)), 2))

#-----------------------------

def main():
    print('\nmain problem:')
    part1, part2 = run(load())
    print('part 1: coordinate = {},{}'.format(*part1))
    print('part 2: identifier = {},{},{}'.format(*part2))

#=============================

if __name__ == '__main__':

    print('\nproblem 11')
    test()
    main()
    print()
