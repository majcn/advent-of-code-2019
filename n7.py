from aocd import data as input_data
from IntcodeRunner import IntcodeRunner
from itertools import permutations


def parse_data():
    return [int(x) for x in input_data.split(',')]


def solve_a(data):
    process_list = permutations(range(5))

    max_result = 0
    for pl in process_list:
        program_output = 0
        for p in pl:
            runner = IntcodeRunner(data, [p, program_output])
            program_output = runner.run()
        max_result = max(max_result, program_output)
    return max_result


def solve_b(data):
    process_list = permutations(range(5, 10))

    max_result = 0
    for pl in process_list:
        program_inputs = {p: [p] for p in pl}
        programs = {p: IntcodeRunner(data, program_inputs[p]) for p in pl}

        program_output = 0
        while not any(programs[p].exit for p in pl):
            for p in pl:
                program_inputs[p].append(program_output)
                program_output = programs[p].run()

        max_result = max(max_result, program_inputs[pl[0]][-1])

    return max_result


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
