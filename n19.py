from aocd import data as input_data
from IntcodeRunner import IntcodeRunner


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_a(data):
    return sum(IntcodeRunner(data, [x, y]).run() for x in range(50) for y in range(50))


def solve_b(data):
    x = 100
    y = 100

    while True:
        y += 1
        while True:
            r = IntcodeRunner(data, [x, y]).run()
            if r == 0:
                x += 1
            else:
                break

        if IntcodeRunner(data, [x + 99, y - 99]).run() != 0:
            return x * 10000 + y - 99


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
