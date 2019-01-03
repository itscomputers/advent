
#   advent/2018/day19.py

import re
import math

#=============================

def load(filename='data/19.txt'):
    with open(filename) as f:
        return parse([x.rstrip() for x in f.readlines()])

#-----------------------------

def parse(data):
    opcodes = []
    ip_pattern = re.compile(r'#ip (\d+)')
    opcode_pattern = re.compile(r'(\w{4}) (\d+) (\d+) (\d+)')
    for line in data:
        if ip_pattern.match(line) is not None:
            pointer = int(ip_pattern.search(line).group(1))
        elif opcode_pattern.match(line) is not None:
            opcode, *args = opcode_pattern.search(line).group(1,2,3,4)
            opcodes.append([opcode, tuple(int(x) for x in args)])
    return pointer, opcodes

#=============================

def addr(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a] + r[b]
    return r

def addi(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a] + b
    return r

def mulr(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a] * r[b]
    return r

def muli(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a] * b
    return r

def banr(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a] & r[b]
    return r

def bani(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a] & b
    return r

def borr(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a] | r[b]
    return r

def bori(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a] | b
    return r

def setr(r_, a, b, c):
    r = [x for x in r_]
    r[c] = r[a]
    return r

def seti(r_, a, b, c):
    r = [x for x in r_]
    r[c] = a
    return r

def gtir(r_, a, b, c):
    r = [x for x in r_]
    r[c] = 1 * (a > r[b])
    return r

def gtri(r_, a, b, c):
    r = [x for x in r_]
    r[c] = 1 * (r[a] > b)
    return r

def gtrr(r_, a, b, c):
    r = [x for x in r_]
    r[c] = 1 * (r[a] > r[b])
    return r

def eqir(r_, a, b, c):
    r = [x for x in r_]
    r[c] = 1 * (a == r[b])
    return r

def eqri(r_, a, b, c):
    r = [x for x in r_]
    r[c] = 1 * (r[a] == b)
    return r

def eqrr(r_, a, b, c):
    r = [x for x in r_]
    r[c] = 1 * (r[a] == r[b])
    return r

#=============================

class Program:

    def __init__(self, pointer, opcodes):
        self.ptr = pointer
        self.opcodes = opcodes
        self.register = [0] * 6
        self.ip = 0
    
    #-------------------------

    def __repr__(self):
        try:
            return 'state: {}\nip: {}\nnext op: {}'\
                .format(self.register, self.ip, self.opcodes[self.ip])
        except IndexError:
            return 'state: {}\nip: {}'\
                .format(self.register, self.ip)

    #-------------------------

    def advance(self):
        opcode, args = self.opcodes[self.ip]
        self.register[self.ptr] = self.ip
        self.register = eval(opcode)(self.register, *args)
        self.ip = self.register[self.ptr] + 1

    #-------------------------

    def run(self):
        while True:
            try:
                self.advance()
            except IndexError:
                break

    #-------------------------

    def signature(self):
        while self.register[4] != 0:
            self.advance()
        while self.ip != 3:
            self.advance()
        return [self.register[i] for i in [0, 2, 3, 5]]

    #-------------------------

    def shortcut(self):
        signature = self.signature()
        num = signature[1]
        self.register = \
                [signature[0] + sum(divisors(num)), 16**2, num, num+1, 1, num+1]
        self.ip = 16**2 + 1

#=============================

def divisors(num):
    divs = [x for x in range(1, int(math.sqrt(num)) + 1) if num % x == 0]
    return sorted(list(set(divs + list(map(lambda d: num//d, divs)))))

#=============================

def test():
    print('\ntests:')
    data = load('test/19.txt')
    p = Program(*data)
    p.run()
    print('part 1: passed {} / 1'.format(1 * (p.register[0] == 6)))

#-----------------------------

def main():
    print('\nmain program:')
    data = load()
    
    p = Program(*data)
    p.shortcut()
    print('part 1: register[0] = {}'.format(p.register[0]))

    p = Program(*data)
    p.register[0] = 1
    p.shortcut()
    print('part 2: register[0] = {}'.format(p.register[0]))

#=============================

if __name__ == '__main__':

    print('\nproblem 19')
    test()
    main()
    print()
