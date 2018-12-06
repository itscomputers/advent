
#   advent/2018/day04.py

import re
from collections import defaultdict

##############################

months = [  '01', '02', '03', '04', '05', '06',
            '07', '08', '09', '10', '11', '12'  ]
days = [    '31', '28', '31', '30', '31', '30',
            '31', '31', '30', '31', '30', '31'  ]

def next_day(date):
    year, month, day = date.split('-')
    if (month, day) in zip(months, days):
        day = '01'
        month = months[(months.index(month) + 1) % 12]
    else:
        day = str(int(day) + 1)
        day = '0' * (len(day) % 2) + day
    if (month, day) == ('01', '01'):
        year = str(int(day) + 1)
    return '{}-{}-{}'.format(year, month, day)

##############################

def parse(data):
    shift_pattern = re.compile(r'Guard #\d*')
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    time_pattern = re.compile(r'\d{2}:\d{2}')
    
    guard_data = dict()
    for line in data:
        date = date_pattern.search(line).group()
        hour, minute = [int(x) for x in \
                time_pattern.search(line).group().split(':')]
        if hour == 23:
            date = next_day(date)
        if date not in guard_data:
            guard_data[date] = {'id' : '', 'asleep' : [], 'awake' : []}
        if shift_pattern.search(line):
            guard_id = int(shift_pattern.search(line).group().lstrip('Guard #'))
            guard_data[date]['id'] = guard_id
        elif 'falls asleep' in line:
            guard_data[date]['asleep'].append(minute)
        elif 'wakes up' in line:
            guard_data[date]['awake'].append(minute)

    return guard_data

##############################

def guard_minutes(data):
    guards = dict()
    for v in data.values():
        if v['id'] not in guards:
            guards[v['id']] = defaultdict(int)
        for start, end in zip(sorted(v['asleep']), sorted(v['awake'])):
            for m in range(start, end):
                guards[v['id']][m] += 1
    return guards

##############################

def best_guard(guards):
    key_one = None
    max_sum = 0
    key_two = None
    max_val = 0
    for k, v in guards.items():
        s = sum(v.values())
        if s > max_sum:
            max_sum = s
            key_one = k
        if len(v.values()) > 0:
            m = max(v.values())
            if m > max_val:
                max_val = m
                key_two = k
    return key_one, key_two

##############################

if __name__ == '__main__':

    with open('data/04.txt') as f:
        guards = guard_minutes(parse(f.readlines()))

    k1, k2 = best_guard(guards)
    for k in [k1, k2]:
        guard = guards[k]
        max_val = max(guards[k].values())
        for minute, value in guards[k].items():
            if value == max_val:
                break
        print(k * minute)
