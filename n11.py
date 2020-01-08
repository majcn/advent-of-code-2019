from aocd import data as input_data
from collections import defaultdict


class IntcodeRunner:
    def __init__(self, program, program_input_generator):
        self.program = defaultdict(int, {i: p for i, p in enumerate(program)})

        self.program_input_generator = program_input_generator

        self.program_output = None

        self.relative_base = 0
        self.c = 0
        self.exit = False

    def opcode(self):
        return self.program[self.c] % 100

    def get_address(self, i):
        mode = (self.program[self.c] // (10 * 10 ** i)) % 10
        if mode == 1:
            return self.c + i
        elif mode == 2:
            return self.relative_base + self.program[self.c + i]
        else:
            return self.program[self.c + i]

    def get_value(self, i):
        return self.program[self.get_address(i)]

    def set_value(self, i, value):
        self.program[self.get_address(i)] = value

    def f1(self):
        p1 = self.get_value(1)
        p2 = self.get_value(2)
        self.set_value(3, p1 + p2)
        self.c += 3

    def f2(self):
        p1 = self.get_value(1)
        p2 = self.get_value(2)
        self.set_value(3, p1 * p2)
        self.c += 3

    def f3(self):
        self.set_value(1, next(self.program_input_generator))
        self.c += 1

    def f4(self):
        p1 = self.get_value(1)
        self.program_output = p1
        self.c += 1

    def f5(self):
        p1 = self.get_value(1)
        p2 = self.get_value(2)
        if p1 != 0:
            self.c = p2 - 1
        else:
            self.c += 2

    def f6(self):
        p1 = self.get_value(1)
        p2 = self.get_value(2)
        if p1 == 0:
            self.c = p2 - 1
        else:
            self.c += 2

    def f7(self):
        p1 = self.get_value(1)
        p2 = self.get_value(2)
        self.set_value(3, 1 if p1 < p2 else 0)
        self.c += 3

    def f8(self):
        p1 = self.get_value(1)
        p2 = self.get_value(2)
        self.set_value(3, 1 if p1 == p2 else 0)
        self.c += 3

    def f9(self):
        p1 = self.get_value(1)
        self.relative_base += p1
        self.c += 1

    def f99(self):
        self.exit = True

    def run(self):
        while not self.exit:
            oc = self.opcode()
            eval('self.f' + str(oc) + '()')
            self.c += 1

            if oc == 4:
                return self.program_output


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
    program = IntcodeRunner(data, iter(program_input))

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
