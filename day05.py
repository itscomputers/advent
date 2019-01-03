
#   advent/2018/day05.py

import re
import string

#=============================

def load(filename='data/05.txt'):
    with open(filename) as f:
        return f.read().rstrip()

#=============================

def match(window):
    if '+' in window or '-' in window:
        return False
    if window[0].lower() != window[1].lower():
        return False
    return re.match(r'[a-z][A-Z]', window) is not None \
            or re.match(r'[A-Z][a-z]', window) is not None

#-----------------------------

def simplified_length(s):
    new_string = ''
    window = '++'
    char = iter(s + '--')
    while '-' not in window:
        if match(window):
            window = new_string[-1] + next(char)
            new_string = new_string[:-1]
        else:
            new_string += window[0]
            window = window[1] + next(char)
    return len(new_string.lstrip('+') + window.rstrip('-'))

#-----------------------------

def remove(string, ch):
    return string.replace(ch, '').replace(ch.upper(), '')

#-----------------------------

def min_length(s):
    return min(l for l in (simplified_length(remove(s, ch)) \
                            for ch in string.ascii_lowercase))

#=============================

def test():
    print('\ntests:')
    string = load('test/05.txt')
    print('part 1: passed {} / 1'.format(
        1 * (simplified_length(string) == 10)))
    print('part 2: passed {} / 1'.format(
        1 * (min_length(string) == 4)))

#-----------------------------

def main():
    print('\nmain problem:')
    string = load()
    print('part 1: polymer length = {}'.format(simplified_length(string)))
    print('part 2: shortest polymer length = {}'.format(min_length(string)))

#=============================

if __name__ == '__main__':

    print('\nproblem 5')
    test()
    main()
    print()
