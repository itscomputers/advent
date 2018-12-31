
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

def test(ch):
    g = grid(load('test/11-{}.txt'.format(ch)))
    squares = squares_by_size(g, vert_sums(g))
    results = {
        'a' : [(33, 45), (90, 269, 16)],
        'b' : [(21, 61), (232, 251, 12)]
    }
    x, y, size, power = max_square_by_size(g, 3, squares)
    test_one = (x, y) == results[ch][0]
    x, y, size, power = max_square(g, squares)
    test_two = (x, y, size) == results[ch][1]
    return test_one, test_two 

#-----------------------------

def main():
    g = grid(load())
    squares = squares_by_size(g, vert_sums(g))
    print('\nmain problem:')
    x, y, size, power = max_square_by_size(g, 3, squares)
    print('part 1: coordinate = {},{}'.format(x, y))
    x, y, size, power = max_square(g, squares)
    print('part 2: identifier = {},{},{}'.format(x, y, size))

#=============================

if __name__ == '__main__':
    tests = [test(ch) for ch in 'ab']
    print('part 1 tests: passed {} / {}'.format(
        sum(1 * t[0] for t in tests), len('ab')))
    print('part 2 tests: passed {} / {}'.format(
        sum(1 * t[1] for t in tests), len('ab')))

    main()
