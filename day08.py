
#   advent/2018/day08.py


##############################

def node_sum(data, problem):
    [c, m, *data] = data
    if c == 0:
        return data[m:], sum(data[:m])

    sums = []
    for i in range(c):
        data, meta_sum = node_sum(data, problem)
        sums.append(meta_sum)
    
    if problem == 1:
        return data[m:], sum(sums) + sum(data[:m])
    else:
        return data[m:], sum(sums[i-1] for i in data[:m] if i <= c)

##############################

def metadata_sum(data, problem=1):
    sums = []
    while data != []:
        data, meta_sum = node_sum(data, problem)
        sums.append(meta_sum)
    if problem == 1:
        return sum(sums)
    else:
        return sums[0]

##############################

if __name__ == '__main__':

    with open('data/08.txt') as f:
        data = [int(x) for x in f.read().split(' ')]

    print(metadata_sum([x for x in data]))
    print(metadata_sum(data, problem=2))
