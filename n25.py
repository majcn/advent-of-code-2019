from aocd import data as input_data
from collections import defaultdict
from itertools import combinations
import re


class IntcodeRunner:
    def __init__(self, program, program_input_generator):
        self.program = defaultdict(int, {i: program[i] for i in range(len(program))})

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


def cmd_robot(program, program_input, cmd):
    s = ''
    if cmd:
        program_input.extend(ord(x) for x in cmd)
        program_input.append(10)
    while True:
        s += chr(program.run())
        if s.endswith('Command?'):
            break

        if s.endswith('on the keypad at the main airlock."'):
            break
    return s


def parse_location_name(s):
    return s.lstrip().split('\n')[0][3:-3]


def parse_paths(s):
    return re.findall(r'^- (north|south|east|west)$', s, re.MULTILINE)


def parse_items(s):
    return re.findall(r'^- (?!north|south|east|west)(.*)$', s, re.MULTILINE)


def reverse_path(path):
    if path == 'north':
        return 'south'
    if path == 'south':
        return 'north'
    if path == 'west':
        return 'east'
    if path == 'east':
        return 'west'


def explore(send_move_cmd_f):
    location_name, paths = send_move_cmd_f(None)

    full_path = ()
    visited = set()
    map_data = {location_name: paths}

    return __explore(location_name, send_move_cmd_f, full_path, map_data, visited)


def __explore(location_name, send_move_cmd_f, full_path, map_data, visited):
    goal_path = ()

    paths = map_data[location_name]

    for path in paths:
        if location_name == 'Security Checkpoint' and path == 'south':
            goal_path = full_path
            continue

        location_name_with_path = f'{location_name} {path}'
        if location_name_with_path in visited:
            continue

        n_location_name, n_paths = send_move_cmd_f(path)
        visited.add(location_name_with_path)
        visited.add(f'{n_location_name} {reverse_path(path)}')
        map_data[n_location_name] = n_paths

        t_goal_path = __explore(n_location_name, send_move_cmd_f, full_path + (path,), map_data, visited)
        if t_goal_path:
            goal_path = t_goal_path

        send_move_cmd_f(reverse_path(path))

    return goal_path


def move_robot_take_items(program, program_input, cmd, banned_items):
    s = cmd_robot(program, program_input, cmd)

    for item in parse_items(s):
        if item not in banned_items:
            cmd_robot(program, program_input, f'take {item}')

    location_name = parse_location_name(s)
    paths = parse_paths(s)
    return location_name, paths


def solve_a(data):
    program_input = []
    program = IntcodeRunner(data, iter(program_input))

    banned_items = {
        'giant electromagnet',
        'infinite loop',
        'escape pod',
        'photons',
        'molten lava'
    }

    goal_path = explore(lambda x: move_robot_take_items(program, program_input, x, banned_items))

    for cmd in goal_path:
        cmd_robot(program, program_input, cmd)

    s = cmd_robot(program, program_input, 'inv')
    items = parse_items(s)

    for item in items:
        cmd_robot(program, program_input, f'drop {item}')

    for i in range(len(items)):
        for item_combination in combinations(items, i + 1):
            for item in item_combination:
                cmd_robot(program, program_input, f'take {item}')
            s = cmd_robot(program, program_input, 'south')

            result = re.search(r'^\"Oh, hello! You should be able to get '
                               r'in by typing (\d+) on the keypad at the '
                               r'main airlock\.\"$', s, re.MULTILINE)
            if result:
                return result.group(1)

            for item in item_combination:
                cmd_robot(program, program_input, f'drop {item}')


print("Part 1: {}".format(solve_a(parse_data())))
