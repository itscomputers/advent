
#   advent/2018/day24.py

import re

#=============================

def load(filename):
    with open(filename) as f:
        return parse([x.rstrip() for x in f.readlines()])

#-----------------------------

def parse(data):
    units_pattern = re.compile(r'(\d+) units')
    hit_pattern = re.compile(r'(\d+) hit points')
    weak_pattern = re.compile(r'weak to ([a-z, ]+)')
    immune_pattern = re.compile(r'immune to ([a-z, ]+)')
    attack_pattern = re.compile(r'attack that does (\d+) ([a-z]+) damage')
    initiative_pattern = re.compile(r'initiative (\d+)')
    immune_system_flag = False
    infection_flag = False
    immune_system = []
    infection = []

    for line in data:

        if 'Immune System:' in line:
            immune_system_flag = True
            infection_flag = False
        elif 'Infection:' in line:
            immune_system_flag = False
            infection_flag = True
        elif units_pattern.search(line) is not None:
            g = Group()
            g.units = int(units_pattern.search(line).group(1))
            g.hit = int(hit_pattern.search(line).group(1))
            g.att_dam = int(attack_pattern.search(line).group(1))
            g.att_type = attack_pattern.search(line).group(2)
            g.initiative = int(initiative_pattern.search(line).group(1))

            if weak_pattern.search(line) is not None:
                g.weak = weak_pattern.search(line).group(1).split(', ')
            if immune_pattern.search(line) is not None:
                g.immune = immune_pattern.search(line).group(1).split(', ')

            if immune_system_flag:
                g.team = 'Immune System'
                immune_system.append(g)
            elif infection_flag:
                g.team = 'Infection'
                infection.append(g)

    return immune_system, infection

#=============================

class Group:

    def __init__(self):
        self.units = None
        self.hit = None
        self.att_dam = None
        self.att_type = None
        self.initiative = None
        self.weak = []
        self.immune = []
        self.target = None

    #-------------------------

    def __repr__(self):
        return '({} units, {} power, {} hit points, {} initiative)'.format(
                self.units, self.power(), self.hit, self.initiative)
    #-------------------------

    def power(self):
        return self.units * self.att_dam

    #-----------------------------

    def damage(self, enemy):
        multiplier = (1 + 1 * (self.att_type in enemy.weak)) \
            * (self.att_type not in enemy.immune)
        return multiplier * self.power()

    #-----------------------------

    def number_killed(self, enemy):
        return self.damage(enemy) // enemy.hit

    #-----------------------------

    def choose_target(self, opponents):
        if self.units == 0 or opponents == []:
            self.target = None
        else:
            self.target = max(opponents,
                key=lambda enemy: (
                    self.damage(enemy),
                    enemy.power(),
                    enemy.initiative))
            if self.damage(self.target) == 0:
                self.target = None

#=============================

def srt(team):
    return sorted(
        team, 
        key=lambda g: (g.power(), g.initiative),
        reverse=True)

#-----------------------------

def choose_targets(team, opponents):
    available = [g for g in opponents if g.units > 0]
    for group in srt(team):
        group.choose_target(available)
        if group.target is not None:
            available.remove(group.target)

#-----------------------------

def advance(immune, infection):
    choose_targets(immune, infection)
    choose_targets(infection, immune)

    attack_groups = sorted(
            [g for g in immune + infection if g.target is not None],
            key=lambda g: g.initiative, reverse=True)
    for group in attack_groups:
        enemy = group.target
        enemy.units -= min(group.number_killed(enemy), enemy.units)

#-----------------------------

def remaining(team):
    return sum(g.units for g in team)

#-----------------------------

def simulate(immune, infection):
    while remaining(immune) != 0 and remaining(infection) != 0:
        advance(immune, infection)

#-----------------------------

def run_simulation(boost, filename):
    immune, infection = load(filename)
    for g in immune:
        g.att_dam += boost
    simulate(immune, infection)
    return remaining(immune), remaining(infection)

#-----------------------------

def find_optimal_boost(filename):
    lower = 0
    lower_sim = run_simulation(lower, filename)[0]

    upper = 2
    upper_sim = run_simulation(upper, filename)[0]

    while True:
        if lower_sim == 0 and upper_sim == 0:
            lower = upper
            lower_sim = upper_sim
            upper *= 2
            upper_sim = run_simulation(upper, filename)[0]
        else:
            break

    guess = lower
    guess_sim = lower_sim
    while upper - lower > 2:
        guess = (upper + lower) // 2
        guess_sim = run_simulation(guess, filename)[0]
        
        if guess_sim == 0:
            lower = guess
            lower_sim = guess_sim
        else:
            upper = guess
            upper_sim = guess_sim

    if guess_sim == 0:
        return upper, upper_sim
    else:
        return guess, guess_sim

#=============================

def run(filename='data/24.txt'):
    rem = run_simulation(0, filename)[1]
    boost, units = find_optimal_boost(filename)
    return rem, units

#-----------------------------

def test():
    print('\ntests:')
    rem, units = run('test/24.txt')
    print('part 1: passed {} / 1'.format(1 * (rem == 5216)))
    print('part 2: passed {} / 1'.format(1 * (units == 51)))

#-----------------------------

def main():
    print('\nmain problem:')
    rem, units = run()
    print('part 1: remaining = {}'.format(rem))
    print('part 2: remaining = {}'.format(units))

#=============================

if __name__ == '__main__':

    print('\nproblem 24')
    test()
    main()
    print()
