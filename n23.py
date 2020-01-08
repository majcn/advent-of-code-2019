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

    def run(self, only_one_opcode=False):
        while not self.exit:
            oc = self.opcode()
            eval('self.f' + str(oc) + '()')
            self.c += 1

            if oc == 4:
                return self.program_output

            if only_one_opcode:
                return None
        return None


def parse_data():
    return [int(x) for x in input_data.split(',')]


class InputGenerator:
    def __init__(self, input_list):
        self.input_list = input_list
        self.i = 0
        self.fallback = False

    def __next__(self):
        if self.i < len(self.input_list):
            self.i += 1
            self.fallback = False
            return self.input_list[self.i - 1]
        else:
            self.fallback = True
            return -1

    def append(self, item):
        self.input_list.append(item)
        self.fallback = False


def solve_x(data, goal_f):
    computers = []
    for i in range(50):
        program_input = InputGenerator([i])
        program = IntcodeRunner(data, program_input)
        computers.append(program)

    counter = 0
    prev_nat = [None, None]
    nat = [None, None]
    while True:
        queue = computers.copy()
        while queue:
            c = queue.pop()
            output = []

            while True:
                v = c.run(only_one_opcode=True)

                if v:
                    output.append(v)

                    if len(output) == 3:
                        a, x, y = output
                        output = []

                        if a == 255:
                            nat = [x, y]
                        else:
                            computers[a].program_input_generator.append(x)
                            computers[a].program_input_generator.append(y)
                            queue.append(computers[a])
                elif c.program_input_generator.fallback:
                    c.program_input_generator.fallback = False
                    break

        if counter % 2 == 1:
            computers[0].program_input_generator.append(nat[0])
            computers[0].program_input_generator.append(nat[1])

            if goal_f(prev_nat, nat):
                return nat[1]
            prev_nat = nat
        counter += 1


def solve_a(data):
    return solve_x(data, lambda pn, n: True)


def solve_b(data):
    return solve_x(data, lambda pn, n: pn[1] == n[1])


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
