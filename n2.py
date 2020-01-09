from aocd import data as input_data
from IntcodeRunner import IntcodeRunner


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_a(data):
    p = IntcodeRunner(data, None)
    p.program[1] = 12
    p.program[2] = 2

    p.run()
    return p.program[0]


def solve_b(data):
    for noun in range(100):
        for verb in range(100):
            p = IntcodeRunner(data, None)
            p.program[1] = noun
            p.program[2] = verb
            p.run()
            if p.program[0] == 19690720:
                return 100 * noun + verb


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
