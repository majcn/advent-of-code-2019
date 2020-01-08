from aocd import data as input_data


class IntcodeRunner:
    def __init__(self, program, program_input_provider, program_output_supplier):
        self.program = {i: p for i, p in enumerate(program)}

        self.program_input_provider = program_input_provider
        self.program_output_supplier = program_output_supplier

        self.c = 0
        self.exit = False

    def opcode(self):
        return self.program[self.c] % 100

    def get_address(self, i):
        mode = (self.program[self.c] // (10 * 10 ** i)) % 10
        if mode == 1:
            return self.c + i
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
        self.set_value(1, self.program_input_provider())
        self.c += 1

    def f4(self):
        p1 = self.get_value(1)
        self.program_output_supplier(p1)
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

    def f99(self):
        self.exit = True

    def run(self):
        while not self.exit:
            oc = self.opcode()
            eval('self.f' + str(oc) + '()')
            self.c += 1


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_a(data):
    result = [None]

    def program_input_provider():
        return 2

    def program_output_supplier(x):
        result[0] = x

    IntcodeRunner(data, program_input_provider, program_output_supplier).run()
    return result[0]


def solve_b(data):
    result = [None]

    def program_input_provider():
        return 5

    def program_output_supplier(x):
        result[0] = x

    IntcodeRunner(data, program_input_provider, program_output_supplier).run()
    return result[0]


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
