
#   advent/2018/day04.py

import re
from collections import defaultdict

#=============================

def load(filename='data/04.txt'):
    with open(filename) as f:
        return parse(f.readlines())

#-----------------------------

def parse(data):
    shift_pattern = re.compile(r'Guard #(\d*)')
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    time_pattern = re.compile(r'(\d{2}):(\d{2})')
    
    guard_data = dict()
    for line in data:
        date = date_pattern.search(line).group()
        hour, minute = [int(x) for x in time_pattern.search(line).group(1,2)]
        if hour == 23:
            date = next_day(date)
        if date not in guard_data:
            guard_data[date] = {'id' : '', 'asleep' : [], 'awake' : []}
        if shift_pattern.search(line):
            guard_id = int(shift_pattern.search(line).group(1))
            guard_data[date]['id'] = guard_id
        elif 'falls asleep' in line:
            guard_data[date]['asleep'].append(minute)
        elif 'wakes up' in line:
            guard_data[date]['awake'].append(minute)

    return guard_data

#=============================

def next_day(date):
    months = [  '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12'  ]
    last_days = [   '31', '28', '31', '30', '31', '30',
                    '31', '31', '30', '31', '30', '31'  ]

    year, month, day = date.split('-')
    if (month, day) in zip(months, last_days):
        day = '01'
        month = months[(months.index(month) + 1) % 12]
    else:
        day = str(int(day) + 1)
        day = '0' * (len(day) % 2) + day
    if (month, day) == ('01', '01'):
        year = str(int(day) + 1)
    return '{}-{}-{}'.format(year, month, day)

#-----------------------------

def guard_minutes(data):
    guards = dict()
    for v in data.values():
        if v['id'] not in guards:
            guards[v['id']] = defaultdict(int)
        for start, end in zip(sorted(v['asleep']), sorted(v['awake'])):
            for m in range(start, end):
                guards[v['id']][m] += 1
    return guards

#-----------------------------

def best_guard(guards):
    key_one = None
    max_sum = 0
    key_two = None
    max_val = 0
    for k, v in guards.items():
        if len(v.values()) > 0:
            s = sum(v.values())
            if s > max_sum:
                max_sum = s
                key_one = k
            m = max(v.values())
            if m > max_val:
                max_val = m
                key_two = k
    return key_one, key_two

#-----------------------------

def process(key, guards):
    guard = guards[key]
    max_val = max(guard.values())
    for minute, value in guard.items():
        if value == max_val:
            break
    return key * minute

#=============================

def test():
    guards = guard_minutes(load('test/04.txt'))
    return tuple(map(lambda x, y: x == y, 
        tuple(process(k, guards) for k in best_guard(guards)), 
        (240, 4455)))

#-----------------------------

def main():
    guards = guard_minutes(load())
    results = [process(key, guards) for key in best_guard(guards)]
    print('\nmain problem:')
    print('part 1: most minutes / best minute: id * min = {}'.format(results[0]))
    print('part 2: most frequent minute: id * min = {}'.format(results[1]))

##############################

if __name__ == '__main__':
    test_one, test_two = test()
    print('part 1 tests: passed {} / 1'.format(1 * test_one))
    print('part 2 tests: passed {} / 1'.format(1 * test_two))

    main()
