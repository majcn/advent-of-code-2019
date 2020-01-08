from aocd import data as input_data


def parse_data():
    return [int(x) for x in input_data.split('\n')]


def solve_a(data):
    return sum(map(lambda x: x // 3 - 2, data))


def solve_b(data):
    r = 0
    while data:
        data = [x // 3 - 2 for x in data if x >= 6]
        r += sum(data)
    return r


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
