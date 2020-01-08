from aocd import data as input_data


def parse_data():
    return {(x, y) for y, line in enumerate(input_data.split('\n')) for x, c in enumerate(line) if c == '#'}


def neighbours_a(l):
    x, y = l
    neighbours = (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)

    return (n for n in neighbours if 0 <= n[0] < 5 and 0 <= n[1] < 5)


def neighbours_b(l):
    x, y, z = l

    if x == 0 and y == 0:
        return (1, 0, z), (0, 1, z), (1, 2, z - 1), (2, 1, z - 1)

    if x == 1 and y == 0:
        return (0, 0, z), (2, 0, z), (1, 1, z), (2, 1, z - 1)

    if x == 2 and y == 0:
        return (1, 0, z), (3, 0, z), (2, 1, z), (2, 1, z - 1)

    if x == 3 and y == 0:
        return (2, 0, z), (4, 0, z), (3, 1, z), (2, 1, z - 1)

    if x == 4 and y == 0:
        return (3, 0, z), (4, 1, z), (2, 1, z - 1), (3, 2, z - 1)

    if x == 0 and y == 1:
        return (0, 0, z), (1, 1, z), (0, 2, z), (1, 2, z - 1)

    if x == 1 and y == 1:
        return (0, 1, z), (1, 0, z), (2, 1, z), (1, 2, z)

    if x == 2 and y == 1:
        return (1, 1, z), (2, 0, z), (3, 1, z), (0, 0, z + 1), (1, 0, z + 1), (2, 0, z + 1), (3, 0, z + 1), (4, 0, z + 1)

    if x == 3 and y == 1:
        return (2, 1, z), (3, 0, z), (4, 1, z), (3, 2, z)

    if x == 4 and y == 1:
        return (3, 1, z), (4, 0, z), (4, 2, z), (3, 2, z - 1)

    if x == 0 and y == 2:
        return (0, 1, z), (1, 2, z), (0, 3, z), (1, 2, z - 1)

    if x == 1 and y == 2:
        return (0, 2, z), (1, 1, z), (1, 3, z), (0, 0, z + 1), (0, 1, z + 1), (0, 2, z + 1), (0, 3, z + 1), (0, 4, z + 1)

    if x == 2 and y == 2:
        return []

    if x == 3 and y == 2:
        return (3, 1, z), (4, 2, z), (3, 3, z), (4, 0, z + 1), (4, 1, z + 1), (4, 2, z + 1), (4, 3, z + 1), (4, 4, z + 1)

    if x == 4 and y == 2:
        return (3, 2, z), (4, 1, z), (4, 3, z), (3, 2, z - 1)

    if x == 0 and y == 3:
        return (0, 2, z), (1, 3, z), (0, 4, z), (1, 2, z - 1)

    if x == 1 and y == 3:
        return (0, 3, z), (1, 2, z), (2, 3, z), (1, 4, z)

    if x == 2 and y == 3:
        return (1, 3, z), (3, 3, z), (2, 4, z), (0, 4, z + 1), (1, 4, z + 1), (2, 4, z + 1), (3, 4, z + 1), (4, 4, z + 1)

    if x == 3 and y == 3:
        return (2, 3, z), (3, 2, z), (4, 3, z), (3, 4, z)

    if x == 4 and y == 3:
        return (3, 3, z), (4, 2, z), (4, 4, z), (3, 2, z - 1)

    if x == 0 and y == 4:
        return (0, 3, z), (1, 4, z), (1, 2, z - 1), (2, 3, z - 1)

    if x == 1 and y == 4:
        return (0, 4, z), (1, 3, z), (2, 4, z), (2, 3, z - 1)

    if x == 2 and y == 4:
        return (1, 4, z), (2, 3, z), (3, 4, z), (2, 3, z - 1)

    if x == 3 and y == 4:
        return (2, 4, z), (3, 3, z), (4, 4, z), (2, 3, z - 1)

    if x == 4 and y == 4:
        return (3, 4, z), (4, 3, z), (3, 2, z - 1), (2, 3, z - 1)


def next_web(web, neighbours_f):
    n_web = set()

    check_items = set()
    for l in web:
        check_items.add(l)
        check_items.update(neighbours_f(l))

    for l in check_items:
        if l in web:
            if sum(n in web for n in neighbours_f(l)) == 1:
                n_web.add(l)
        else:
            tmp = sum(n in web for n in neighbours_f(l))
            if tmp == 1 or tmp == 2:
                n_web.add(l)

    return n_web


def solve_a(data):
    cache = set()
    web = frozenset(data)

    while web not in cache:
        cache.add(web)
        web = frozenset(next_web(web, neighbours_a))

    return sum(pow(2, (y * 5 + x)) for x, y in web)


def solve_b(data):
    web = {(d[0], d[1], 0) for d in data}
    for x in range(200):
        web = next_web(web, neighbours_b)
    return len(web)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
