from aocd import data as input_data
from collections import defaultdict
from collections import deque
from itertools import combinations
import heapq


def parse_data():
    grid = set()
    doors = {}
    keys = {}
    start = None
    for y, line in enumerate(input_data.split('\n')):
        for x, c in enumerate(line):
            if c == '.':
                grid.add((x, y))
            elif c == '@':
                start = (x, y)
                grid.add((x, y))
            elif c.isupper():
                doors[(x, y)] = c.lower()
                grid.add((x, y))
            elif c.islower():
                keys[(x, y)] = c.lower()
                grid.add((x, y))

    keys_mask = defaultdict(int)
    c = 1
    for k in keys:
        keys_mask[k] = c
        keys_mask[keys[k]] = c
        c *= 2

    return start, doors, keys, keys_mask, grid


def bfs(start, finish, grid):
    def get_neighbors(location):
        x, y = location
        neighbors = (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)

        return (n for n in neighbors if n in grid)

    q = deque([(0, start)])
    came_from = {start: None}
    while q:
        cost, current = q.popleft()

        if current == finish:
            return cost, came_from

        for neighbor in get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                q.append((cost + 1, neighbor))


def get_my_grid(start, doors, keys, keys_mask, grid):
    my_grid = defaultdict(list)
    for k1, k2 in combinations(keys.keys() | set(start), 2):
        bfs_result = bfs(k1, k2, grid)

        if not bfs_result:
            continue

        cost, came_from = bfs_result
        keys_needed = 0

        current = k2
        while current in came_from:
            current = came_from[current]
            if current in doors:
                keys_needed += keys_mask[doors[current]]
        my_grid[k1].append((k2, cost, keys_needed))
        my_grid[k2].append((k1, cost, keys_needed))

    return my_grid


def shortest_path(start, my_grid, keys_mask, goal_f):
    first_element = (start, 0)

    open_queue = [(0, first_element)]
    score = {first_element: 0}

    while open_queue:
        cost, current = heapq.heappop(open_queue)

        if goal_f(current):
            return cost

        locations, my_keys = current

        for i in range(len(locations)):
            for n_location, n_cost, keys_needed in my_grid[locations[i]]:
                if keys_needed & my_keys != keys_needed:
                    continue

                if my_keys & keys_mask[n_location] > 0:
                    continue

                n_locations = list(locations)
                n_locations[i] = n_location
                neighbor = (tuple(n_locations), my_keys | keys_mask[n_location])

                tentative_score = score[current] + n_cost
                if neighbor not in score or tentative_score < score[neighbor]:
                    score[neighbor] = tentative_score
                    heapq.heappush(open_queue, (tentative_score, neighbor))


def solve_a(data):
    start, doors, keys, keys_mask, grid = data

    start = (start,)
    goal = sum(keys_mask.values()) // 2

    my_grid = get_my_grid(start, doors, keys, keys_mask, grid)
    return shortest_path(start, my_grid, keys_mask, lambda c: c[1] == goal)


def solve_b(data):
    start, doors, keys, grid, keys_mask = data

    x, y = start
    grid.remove((x, y))
    grid.remove((x - 1, y))
    grid.remove((x + 1, y))
    grid.remove((x, y - 1))
    grid.remove((x, y + 1))

    start = (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)
    goal = sum(keys_mask.values()) // 2

    my_grid = get_my_grid(start, doors, keys, keys_mask, grid)
    return shortest_path(start, my_grid, keys_mask, lambda c: c[1] == goal)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
