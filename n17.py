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


def get_grid(data):
    program = IntcodeRunner(data, None)

    start = None

    grid = set()
    x = 0
    y = 0
    while True:
        o = program.run()

        if program.exit:
            break

        c = chr(o)
        if c == '.':
            x += 1
        elif c == '#':
            grid.add((x, y))
            x += 1
        elif c == '^':
            start = (x, y)
            grid.add((x, y))
            x += 1
        elif c == '\n':
            x = 0
            y += 1

    return start, grid


def get_path(start, grid):
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

    result = ''
    direction = 0
    location = start
    counter = 0
    while True:
        n_location = next_location[direction](*location)
        if n_location in grid:
            counter += 1
            location = n_location
        else:
            n_location = None
            n_direction = None

            # check left
            n_direction_l = next_direction[direction, 0]
            n_location_l = next_location[n_direction_l](*location)
            if n_location_l in grid:
                n_location = n_location_l
                n_direction = n_direction_l
                result += str(counter) + ",L,"

            # check right
            n_direction_r = next_direction[direction, 1]
            n_location_r = next_location[n_direction_r](*location)
            if n_location_r in grid:
                n_location = n_location_r
                n_direction = n_direction_r
                result += str(counter) + ",R,"

            if not n_location:
                result += str(counter)
                return result[2:]

            location = n_location
            direction = n_direction
            counter = 1


def solve_a(data):
    start, grid = get_grid(data)

    result = 0
    for x, y in grid:
        is_intersection = True
        for l in [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if l not in grid:
                is_intersection = False
                break
        if is_intersection:
            result += x * y
    return result


def solve_b(data):
    # start, grid = get_grid(data)
    # path = get_path(start, grid)
    # print(path)

    def transform_to_input(m):
        return [ord(x) for x in m] + [10]

    # done by hand
    m_a = transform_to_input('L,10,R,8,R,6,R,10')
    m_b = transform_to_input('L,12,R,8,L,12')
    m_c = transform_to_input('L,10,R,8,R,8')
    m_p = transform_to_input('A,B,A,B,C,C,B,A,C,A')
    program_input = m_p + m_a + m_b + m_c + transform_to_input('n')

    program = IntcodeRunner(data, iter(program_input))
    program.program[0] = 2
    result = None
    while True:
        tmp = program.run()
        if program.exit:
            return result
        result = tmp


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
