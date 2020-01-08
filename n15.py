from aocd import data as input_data
from collections import defaultdict
from collections import deque


class IntcodeRunner:
    def __init__(self, program, program_input_generator):
        self.program = defaultdict(int, {i: program[i] for i in range(len(program))})

        self.program_input_generator = program_input_generator

        self.program_output = None

        self.relative_base = 0
        self.c = 0
        self.exit = False

    def copy(self):
        r = IntcodeRunner(self.program, self.program_input_generator)

        r.relative_base = self.relative_base
        r.c = self.c
        r.exit = self.exit

        return r

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
    program_input = []
    program = IntcodeRunner(data, iter(program_input))

    state_free = 0
    state_wall = 1

    output_moved = 1
    output_goal = 2

    grid = {}
    start = (0, 0)
    goal = None

    open_set = [(start, program, None)]
    visited = set()
    while open_set:
        current = open_set.pop()

        location, p, p_output_state = current

        if p_output_state == output_goal:
            grid[location] = state_free
            goal = location
        elif p_output_state == output_moved:
            grid[location] = state_free
        else:
            grid[location] = state_wall

        neighbors = [
            ((location[0], location[1] - 1), 1),
            ((location[0], location[1] + 1), 2),
            ((location[0] - 1, location[1]), 3),
            ((location[0] + 1, location[1]), 4)
        ]

        for n_location, n_p_input in neighbors:
            n_p = p.copy()

            program_input.append(n_p_input)
            n_p_output_state = n_p.run()

            if n_p_output_state == output_moved or n_p_output_state == output_goal:
                if n_location not in visited:
                    visited.add(n_location)
                    open_set.append((n_location, n_p, n_p_output_state))

    return start, goal, grid


def get_valid_neighbors(grid, location):
    x, y = location
    neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
    return [n for n in neighbors if n in grid and grid[n] == 0]


def solve_a(data):
    start, goal, grid = get_grid(data)

    open_set = deque([start])
    score = {start: 0}
    while open_set:
        location = open_set.popleft()

        if location == goal:
            return score[location]

        for n_location in get_valid_neighbors(grid, location):
            tentative_score = score[location] + 1
            if n_location not in score or tentative_score < score[n_location]:
                score[n_location] = tentative_score
                open_set.append(n_location)


def solve_b(data):
    start, goal, grid = get_grid(data)

    open_set = [(goal, 0)]
    visited = set()
    max_c = 0
    while open_set:
        location, c = open_set.pop()
        max_c = max(max_c, c)

        for n_location in get_valid_neighbors(grid, location):
            if n_location not in visited:
                open_set.append((n_location, c + 1))
                visited.add(n_location)
    return max_c


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
