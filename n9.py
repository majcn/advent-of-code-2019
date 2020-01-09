from aocd import data as input_data
from IntcodeRunner import IntcodeRunner


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_a(data):
    return IntcodeRunner(data, [1]).run()


def solve_b(data):
    return IntcodeRunner(data, [2]).run()


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
