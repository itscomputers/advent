
#   advent/2018/day15.py

from functools import reduce

##############################

def other(kind):
    return 'G' * (kind == 'E') + 'E' * (kind == 'G')

##############################

def nbhd(pos, loc):
    x, y = pos
    return [nb for nb in [(x,y-1), (x,y+1), (x-1,y), (x+1,y)] if nb in loc] 

##############################

def open_nbhd(pos, loc):
    return [nb for nb in nbhd(pos, loc) if loc[nb] is None]

##############################

def dist_to_other(pos, kind, loc):
    circles = [set([pos])]
    visited = circles[0]
    radius = 0
    while True:
        radius += 1
        circle = set(reduce(
            lambda x, y: x + y,
            [[nb for nb in nbhd(p, loc) if nb not in visited] \
                for p in circles[-1]],
            []))
        for p in circle:
            if loc[p] is not None and loc[p].kind == other(kind):
                return radius
        circle = set(p for p in circle if loc[p] is None)
        if circle == set():
            return None
        visited = visited | circle
        circles.append(circle)

##############################

def best_path(pos, kind, loc):
    if dist_to_other(pos, kind, loc) is None:
        return pos
    options = [(dist_to_other(nb, kind, loc), nb) for nb in open_nbhd(pos, loc)]
    options = [(d, nb) for (d, nb) in options if d is not None]
    if options == []:
        return pos
    return min(options, key=lambda t: (t[0], t[1][1], t[1][0]))[1]

##############################

class Creature:

    def __init__(self, kind, pos, ap, hp):
        self.kind = kind
        self.other = other(kind)
        self.pos = pos
        self.ap = ap
        self.hp = hp
        self.enemies = []

    def __repr__(self):
        return '{}({})'.format(self.kind, self.hp)
    
    def move(self, loc):
        if self.enemies == []:
            new_pos = best_path(self.pos, self.kind, loc)
            loc[self.pos] = None
            loc[new_pos] = self
            self.pos = new_pos


    def update(self, loc):
        self.enemies = [loc[nb] for nb in nbhd(self.pos, loc) \
                            if loc[nb] is not None \
                            and loc[nb].kind == self.other \
                            and loc[nb].hp > 0]

    def attack(self):
        if self.enemies != [] and self.hp > 0:
            enemy = min(self.enemies, key=lambda e: (e.hp, e.pos[1], e.pos[0]))
            enemy.hp -= self.ap

##############################

class Cavern:

    def __init__(self, data, elf_ap):
        self.data = data
        self.elf_ap = elf_ap
        self.loc = dict()
        self.parse()
        self.xmin = min(l[0] for l in self.loc.keys())
        self.xmax = max(l[0] for l in self.loc.keys())
        self.ymin = min(l[1] for l in self.loc.keys())
        self.ymax = max(l[1] for l in self.loc.keys())
        for pos, creature in self.creatures():
            creature.update(self.loc)
        self.partial = False

    def __repr__(self):
        lines = []
        for y in range(self.ymin - 1, self.ymax + 2):
            line = '  '
            for x in range(self.xmin - 1, self.xmax + 2):
                if (x,y) not in self.loc:
                    line += '#'
                elif self.loc[x,y] is None:
                    line += '.'
                else:
                    line += self.loc[x,y].kind
            for x in range(self.xmin, self.xmax + 1):
                if (x,y) in self.loc and self.loc[(x,y)] is not None:
                    line += '  {}'.format(self.loc[(x,y)])
            lines.append(line)
        return '\n' + '\n'.join(lines) + '\n'

    def parse(self):
        for y, line in enumerate(self.data):
            for x, ch in enumerate(line):
                if ch == '.':
                    self.loc[(x,y)] = None
                elif ch == 'G':
                    self.loc[(x,y)] = Creature(ch, (x,y), 3, 200)
                elif ch == 'E':
                    self.loc[(x,y)] = Creature(ch, (x,y), self.elf_ap, 200)

    def creatures(self):
        return sorted([(pos, cr) for pos, cr in self.loc.items() \
                        if cr is not None and cr.hp > 0],
                        key=lambda t: (t[0][1], t[0][0]))
    
    def kinds(self):
        return {ch : sum(1 for pos, cr in self.creatures() if cr.kind == ch) \
                for ch in ['E', 'G']}

    def advance(self):
        for pos, creature in self.creatures():
            creature.update(self.loc)
            creature.move(self.loc)
            creature.update(self.loc)
            creature.attack()
            for e in creature.enemies:
                if e.hp < 1:
                    self.loc[e.pos] = None
            creature.update(self.loc)
            if 0 in self.kinds().values() \
                    and creature != self.creatures()[-1][1]:
                self.partial = True

##############################

def game(data, elf_ap):
    index = 0
    cavern = Cavern(data, elf_ap)
    while 0 not in cavern.kinds().values():
        cavern.advance()
        index += 1
    score = sum(cr.hp for pos, cr in cavern.creatures())
    outcome = (index - cavern.partial * 1) * score
    num_elves = cavern.kinds()['E']
    return index, score, outcome, num_elves, cavern

##############################

def find_elf_attack_power(data):
    elf_ap = 4
    num_elves = Cavern(data, elf_ap).kinds()['E']
    while True:
        i, s, o, n, c = game(data, elf_ap)
        if n == num_elves:
            break
        elf_ap += 1
    return elf_ap

##############################

if __name__ == '__main__':

    with open('data/15.txt') as f:
        data = [x.rstrip() for x in f.readlines()]

    print('even match outcome:', game(data, 3)[2])
    
    elf_ap = find_elf_attack_power(data)
    print('with elf attack {}, outcome: {}'\
            .format(elf_ap, game(data, elf_ap)[2]))
