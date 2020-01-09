from aocd import data as input_data
from IntcodeRunner import IntcodeRunner


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_x(data, commands):
    program_input = []
    for command in commands:
        program_input.extend(ord(x) for x in command)
        program_input.append(10)

    program = IntcodeRunner(data, program_input)
    while True:
        r = program.run()
        if r > 255:
            return r


def solve_a(data):
    # done by hand (Truth table)
    commands = [
        'NOT A J',
        'NOT B T',
        'AND D T',
        'OR T J',
        'NOT C T',
        'AND A T',
        'AND B T',
        'AND D T',
        'OR T J',
        'WALK'
    ]

    return solve_x(data, commands)


def solve_b(data):
    # done by hand (Truth table)
    commands = [
        'NOT A J',
        'NOT B T',
        'AND D T',
        'OR T J',
        'NOT C T',
        'AND A T',
        'AND B T',
        'AND D T',
        'AND H T',
        'OR T J',
        'RUN'
    ]

    return solve_x(data, commands)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
