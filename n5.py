from aocd import data as input_data
from IntcodeRunner import IntcodeRunner


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_a(data):
    p = IntcodeRunner(data, [2])
    while True:
        r = p.run()
        if r > 0:
            return r


def solve_b(data):
    return IntcodeRunner(data, [5]).run()


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
