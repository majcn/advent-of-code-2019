from aocd import data as input_data
from IntcodeRunner import IntcodeRunner
from collections import defaultdict


def parse_data():
    return [int(x) for x in input_data.split(',')]


def get_painted_grid(data, starting_color):
    next_direction = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 0): 0,
        (1, 1): 2,
        (2, 0): 1,
        (2, 1): 3,
        (3, 0): 2,
        (3, 1): 0
    }

    next_location = {
        0: lambda x, y: (x, y - 1),
        1: lambda x, y: (x + 1, y),
        2: lambda x, y: (x, y + 1),
        3: lambda x, y: (x - 1, y),
    }

    location = (0, 0)
    direction = 0
    grid = defaultdict(int)
    grid[location] = starting_color
    program_input = []
    program = IntcodeRunner(data, program_input)

    while True:
        program_input.append(grid[location])
        r = program.run(), program.run()
        if program.exit:
            return grid
        grid[location] = r[0]
        direction = next_direction[direction, r[1]]
        location = next_location[direction](*location)


def solve_a(data):
    return len(get_painted_grid(data, 0))


def solve_b(data):
    grid = get_painted_grid(data, 1)

    mmin = min(min(x for x, y in grid), min(y for x, y in grid))
    mmax = max(max(x for x, y in grid), max(y for x, y in grid))
    s = "\n"
    for y in range(mmin, mmax):
        for x in range(mmin, mmax):
            s += "█" if grid[(x, y)] == 1 else " "
        s += "\n"

    return s.rstrip()


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
