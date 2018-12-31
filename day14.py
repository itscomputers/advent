
#   advent/2018/day14.py

#=============================

def load(filename='data/14.txt'):
    with open(filename) as f:
        return f.read().rstrip()

#=============================

class Recipe:

    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def __repr__(self):
        return format(self.val)
    
    def advance(self):
        r = self
        for i in range(self.val + 1):
            r = r.next
        return r

#=============================

class Queue:

    def __init__(self, *vals):
        a, b = vals
        r0 = Recipe(a)
        r1 = Recipe(b)
        r0.next = r1
        r0.prev = r1
        r1.next = r0
        r1.prev = r0
        self.first = r0
        self.last = r1
        self.recipes = (r0, r1)
        self.length = 2

    def __repr__(self):
        return '{}\n{}\n{}'.format(
            'length: {}'.format(self.length),
            'current recipes: {}, {}'.format(*self.recipes),
            'last: ...{}'.format(self.nth_last(11)))

    def advance(self):
        num = sum(r.val for r in self.recipes)
        if num > 9:
            vals = [num // 10, num % 10]
            self.length += 2
        else:
            vals = [num]
            self.length += 1

        for val in vals:
            r = Recipe(val)
            r.next = self.first
            self.first.prev = r
            self.last.next = r
            r.prev = self.last
            self.last = r

        self.recipes = tuple(r.advance() for r in self.recipes)

    def nth_last(self, num):
        arr = [self.last]
        for i in range(min(num -1, self.length - 1)):
            arr.append(arr[-1].prev)
        return '{}{}'.format(
                '...' * (num < self.length),
                ''.join(str(x.val) for x in reversed(arr)))

#=============================
        
def next_ten_after(num):
    q = Queue(3,7)
    while q.length < num + 10:
        q.advance()
    if q.length == num + 10:
        return q.nth_last(10)[-10:]
    else:
        return q.nth_last(11)[-11:-1]

#-----------------------------

def find(string):
    l = len(string)
    q = Queue(3, 7)
    while True:
        q.advance()
        if string == q.nth_last(l)[-l:]:
            return q.length - l
        elif string == q.nth_last(l+1)[-l-1:-1]:
            return q.length - l - 1

#=============================

def test1(ch):
    data = load('test/14-{}.txt'.format(ch))
    results = {
        'a' : '5158916779',
        'b' : '0124515891',
        'c' : '9251071085',
        'd' : '5941429882'
    }
    return next_ten_after(int(data)) == results[ch]

#-----------------------------

def test2(ch):
    data = load('test/14-{}.txt'.format(ch))
    results = {
        'e' : 9,
        'f' : 5,
        'g' : 18,
        'h' : 2018
    }
    return find(data) == results[ch]

#-----------------------------

def main():
    data = load()
    print('\nmain problem:')
    print('part 1: next ten = {}'.format(next_ten_after(int(data))))
    print('part 2: number of recipes = {}'.format(find(data)))

#=============================

if __name__ == '__main__':
    print('part 1 tests: passed {} / {}'.format(
        sum(1 * test1(ch) for ch in 'abcd'), len('abcd')))
    print('part 2 tests: passed {} / {}'.format(
        sum(1 * test2(ch) for ch in 'efgh'), len('efgh')))

    main()
