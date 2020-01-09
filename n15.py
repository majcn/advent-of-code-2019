from aocd import data as input_data
from IntcodeRunner import IntcodeRunner
from collections import deque


def parse_data():
    return [int(x) for x in input_data.split(',')]


def move_robot(program, program_input, cmd):
    output_moved = 1
    output_goal = 2

    program_input.append(cmd)
    n_p_output_state = program.run()

    if n_p_output_state == output_moved or n_p_output_state == output_goal:
        return True, n_p_output_state == output_goal

    return False, False


def explore(location, send_move_cmd_f, visited=None):
    grid = set()
    goal = set()

    if visited is None:
        visited = set()

    neighbors = (
        ((location[0], location[1] - 1), 1, 2),
        ((location[0], location[1] + 1), 2, 1),
        ((location[0] - 1, location[1]), 3, 4),
        ((location[0] + 1, location[1]), 4, 3)
    )

    for n_location, n_p_input, n_r_p_input in neighbors:
        if n_location in visited:
            continue

        has_moved, found_goal = send_move_cmd_f(n_p_input)
        visited.add(n_location)

        if found_goal:
            goal.add(n_location)

        if has_moved:
            grid.add(n_location)
            n_grid, n_goal = explore(n_location, send_move_cmd_f, visited)
            grid.update(n_grid)
            goal.update(n_goal)

            send_move_cmd_f(n_r_p_input)

    return grid, goal


def get_grid(data):
    start = (0, 0)
    program_input = []
    program = IntcodeRunner(data, program_input)
    grid, goal = explore(start, lambda x: move_robot(program, program_input, x))

    return start, goal.pop(), grid


def get_valid_neighbors(grid, location):
    x, y = location
    neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
    return [n for n in neighbors if n in grid]


def solve_a(data):
    start, goal, grid = get_grid(data)

    open_set = deque([(0, start)])
    visited = set()
    while open_set:
        cost, location = open_set.popleft()

        if location == goal:
            return cost

        for n_location in get_valid_neighbors(grid, location):
            if n_location not in visited:
                open_set.append((cost + 1, n_location))
                visited.add(n_location)


def solve_b(data):
    start, goal, grid = get_grid(data)

    open_set = [(0, goal)]
    visited = set()
    max_c = 0
    while open_set:
        cost, location = open_set.pop()
        max_c = max(max_c, cost)

        for n_location in get_valid_neighbors(grid, location):
            if n_location not in visited:
                open_set.append((cost + 1, n_location))
                visited.add(n_location)
    return max_c


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
