from aocd import data as input_data
from IntcodeRunner import IntcodeRunner


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
