
#   advent/2018/day21.py

import re
import math

#=============================

def load(filename='data/21.txt'):
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

    def __init__(self, register_zero, pointer, opcodes):
        self.ptr = pointer
        self.opcodes = opcodes
        self.register = [register_zero] + [0] * 5
        self.ip = 0

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

    def run_to(self, ip):
        while self.ip != ip:
            self.advance()

    #-------------------------

    def loop18(self):
        if self.ip == 18 and 256 * (self.register[3] + 1) <= self.register[5]:
            self.register[3] = self.register[5] // 256

    #-------------------------

    def loop13(self):
        if self.ip == 13 and 256 <= self.register[5]:
            self.run_to(18)
            self.loop18()
            self.run_to(13)
            
    #-------------------------

    def next_register_one(self):
        self.run_to(13)
        while self.register[5] > 255:
            self.loop13()
        self.run_to(28)
        return self.register[1]

#=============================

def main():

    print('\nmain program:')
    data = load()
    p = Program(0, *data)
    
    p.run_to(28)
    vals = [p.register[1]]
    print('part 1: register[0] = {}'.format(vals[0]))

    while True:
        v = p.next_register_one()
        if v in vals:
            break
        else:
            vals.append(v)
    print('part 2: register[0] = {}'.format(vals[-1]))

##############################

if __name__ == '__main__':

    print('\nproblem 21')
    print('\nno tests')
    main()
    print()
