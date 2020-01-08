from aocd import data as input_data
from collections import deque


def parse_data():
    grid = set()
    letters = {}

    grid_height = len(input_data.split('\n'))
    grid_width = len(input_data.split('\n')[0])

    for y, line in enumerate(input_data.split('\n')):
        for x, c in enumerate(line):
            if c == '.':
                grid.add((x, y))
            if c.isalpha():
                letters[(x, y)] = c

    outer_portals = {}
    inner_portals = {}

    for x, y in letters:
        if (x + 1, y) in letters and (x + 2, y) in grid:
            name = letters[(x, y)] + letters[(x + 1, y)]
            if x == 0:
                outer_portals[name] = x + 2, y
            else:
                inner_portals[name] = x + 2, y

        if (x - 1, y) in letters and (x - 2, y) in grid:
            name = letters[(x - 1, y)] + letters[(x, y)]
            if x == grid_width - 1:
                outer_portals[name] = x - 2, y
            else:
                inner_portals[name] = x - 2, y

        if (x, y + 1) in letters and (x, y + 2) in grid:
            name = letters[(x, y)] + letters[(x, y + 1)]
            if y == 0:
                outer_portals[name] = x, y + 2
            else:
                inner_portals[name] = x, y + 2

        if (x, y - 1) in letters and (x, y - 2) in grid:
            name = letters[(x, y - 1)] + letters[(x, y)]
            if y == grid_height - 1:
                outer_portals[name] = x, y - 2
            else:
                inner_portals[name] = x, y - 2

    for n in list(outer_portals):
        outer_portals[outer_portals[n]] = n

    for n in list(inner_portals):
        inner_portals[inner_portals[n]] = n

    start = outer_portals['AA']
    del outer_portals[outer_portals['AA']]
    del outer_portals['AA']

    end = outer_portals['ZZ']
    del outer_portals[outer_portals['ZZ']]
    del outer_portals['ZZ']

    return grid, start, end, outer_portals, inner_portals


def neighbors_a(grid, outer_portals, inner_portals, location):
    x, y = location
    neighbors = (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)

    result = []
    for n in neighbors:
        if n in inner_portals:
            result.append((2, outer_portals[inner_portals[n]]))
        elif n in outer_portals:
            result.append((2, inner_portals[outer_portals[n]]))
        elif n in grid:
            result.append((1, n))
    return result


def neighbors_b(grid, outer_portals, inner_portals, location):
    x, y, z = location
    neighbors = (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)

    result = []
    for n in neighbors:
        if n in inner_portals:
            tmp = outer_portals[inner_portals[n]]
            result.append((2, (tmp[0], tmp[1], z + 1)))
        elif n in outer_portals and z > 0:
            tmp = inner_portals[outer_portals[n]]
            result.append((2, (tmp[0], tmp[1], z - 1)))
        elif n in grid:
            result.append((1, (n[0], n[1], z)))
    return result


def shortest_path(start, neighbors_f, goal_f):
    open_set = deque([start])
    score_map = {start: 0}

    while open_set:
        current = open_set.popleft()

        if goal_f(current):
            return score_map[current]

        for cost, neighbor in neighbors_f(current):
            tentative_score = score_map[current] + cost
            if neighbor not in score_map or tentative_score < score_map[neighbor]:
                score_map[neighbor] = tentative_score
                open_set.append(neighbor)


def solve_a(data):
    grid, start, end, outer_portals, inner_portals = data

    def neighbors_f(location):
        return neighbors_a(grid, outer_portals, inner_portals, location)

    def goal_f(location):
        return location == end

    return shortest_path(start, neighbors_f, goal_f)


def solve_b(data):
    grid, start, end, outer_portals, inner_portals = data

    start = (start[0], start[1], 0)
    end = (end[0], end[1], 0)

    def neighbors_f(location):
        return neighbors_b(grid, outer_portals, inner_portals, location)

    def goal_f(location):
        return location == end

    return shortest_path(start, neighbors_f, goal_f)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
