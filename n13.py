from aocd import data as input_data
from IntcodeRunner import IntcodeRunner


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_a(data):
    program = IntcodeRunner(data, None)
    c = 0
    while not program.exit:
        x, y, tile_id = program.run(), program.run(), program.run()
        if tile_id == 2:
            c += 1
    return c


def solve_b(data):
    ball_x = 0
    paddle_x = 0

    def program_input_generator():
        while True:
            if paddle_x > ball_x:
                yield -1
            elif paddle_x == ball_x:
                yield 0
            else:
                yield 1

    program = IntcodeRunner(data, program_input_generator())
    program.program[0] = 2

    score = 0
    while True:
        x, y, tile_id = program.run(), program.run(), program.run()
        if program.exit:
            return score

        if x == -1 and y == 0:
            score = tile_id
        elif tile_id == 3:
            paddle_x = x
        elif tile_id == 4:
            ball_x = x


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
