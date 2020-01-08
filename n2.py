from aocd import data as input_data


class IntcodeRunner:
    def __init__(self, program):
        self.program = {i: p for i, p in enumerate(program)}

        self.c = 0
        self.exit = False

    def opcode(self):
        return self.program[self.c]

    def get_address(self, i):
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

    def f99(self):
        self.exit = True

    def run(self):
        while not self.exit:
            oc = self.opcode()
            eval('self.f' + str(oc) + '()')
            self.c += 1

        return self.program


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_a(data):
    p = IntcodeRunner(data)
    p.program[1] = 12
    p.program[2] = 2

    return p.run()[0]


def solve_b(data):
    for noun in range(100):
        for verb in range(100):
            p = IntcodeRunner(data)
            p.program[1] = noun
            p.program[2] = verb
            if p.run()[0] == 19690720:
                return 100 * noun + verb


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
