
#   advent/2018/day14.py

##############################

class Recipe:

    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None
    
    def advance(self):
        r = self
        for i in range(self.val + 1):
            r = r.next
        return r

##############################

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
        current = tuple(r.val for r in self.recipes)
        return '{}\n{}\n{}'.format(
            'length: {}'.format(self.length),
            'current recipes: {}, {}'.format(*current),
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

##############################
        
def next_ten_after(num):
    q = Queue(3,7)
    while q.length < num + 10:
        q.advance()
    if q.length == num + 10:
        return q.nth_last(10)[-10:]
    else:
        return q.nth_last(11)[-11:-1]

##############################

def find(string):
    l = len(string)
    q = Queue(3, 7)
    while True:
        q.advance()
        if string == q.nth_last(l)[-l:]:
            return q.length - l
        elif string == q.nth_last(l+1)[-l-1:-1]:
            return q.length - l - 1

##############################

if __name__ == '__main__':

    with open('data/14.txt') as f:
        data = f.read().rstrip()

    print(next_ten_after(int(data)))

    print(find(data))
