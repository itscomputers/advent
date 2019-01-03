
#   advent/2018/day16.py

import re

#=============================

def load(filename='data/16.txt'):
    with open(filename) as f:
        return parse(f.readlines())

#-----------------------------

def parse(data):
    before_pattern = re.compile('Before: \[(\d+), (\d+), (\d+), (\d+)\]')
    after_pattern = re.compile('After:  \[(\d+), (\d+), (\d+), (\d+)\]')
    opcode_pattern = re.compile('(\d+) (\d+) (\d+) (\d+)')
    inputs = []
    outputs = []
    opcodes = []
    for line in data:
        if before_pattern.search(line) is not None:
            inputs.append(before_pattern.search(line).group(1,2,3,4))
        if after_pattern.search(line) is not None:
            outputs.append(after_pattern.search(line).group(1,2,3,4))
        if opcode_pattern.search(line) is not None:
            opcodes.append(opcode_pattern.search(line).group(1,2,3,4))
    inputs = [[int(x) for x in i] for i in inputs]
    outputs = [[int(x) for x in i] for i in outputs]
    opcodes = [[int(x) for x in i] for i in opcodes]
    samples = [(inputs[i], opcodes[i], outputs[i]) for i in range(len(inputs))]
    instructions = opcodes[len(inputs):]
    return samples, instructions

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

opcodes = [
    addr, addi,
    mulr, muli,
    banr, bani,
    borr, bori,
    setr, seti,
    gtir, gtri, gtrr,
    eqir, eqri, eqrr
]

#=============================

class Opcodes:

    def __init__(self, samples):
        self.dict = dict()
        for i, [n,a,b,c], o in samples:
            if n in self.dict:
                self.dict[n] = [op for op in self.dict[n] if op(i,a,b,c) == o]
            else:
                self.dict[n] = [op for op in opcodes if op(i,a,b,c) == o]
        while self.determined() != list(range(16)):
            self.reduce()
        for n, v in self.dict.items():
            self.dict[n] = v[0]

    def determined(self):
        return [n for n, ops in self.dict.items() if len(ops) == 1]

    def reduce(self):
        for n in self.determined():
            op = self.dict[n][0]
            for m in self.dict:
                if m not in self.determined() and op in self.dict[m]:
                    self.dict[m].remove(op)

#=============================

def ambiguous(samples):
        return sum(1 for i, [n,a,b,c], o in samples \
                    if len([op for op in opcodes if op(i,a,b,c) == o]) > 2)

#=============================

def test():
    print('\nno tests')

def main():
    print('\nmain problem:')
    samples, instructions = load()
    print('part 1: ambiguous samples = {}'.format(ambiguous(samples)))
    opcd = Opcodes(samples).dict
    r = [0, 0, 0, 0]
    for [n, a, b, c] in instructions:
        r = opcd[n](r, a, b, c)
    print('part 2: register[0] = {}'.format(r[0]))

#=============================

if __name__ == '__main__':

    print('\nproblem 16')
    test()
    main()
    print()
