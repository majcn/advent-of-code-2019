from aocd import data as input_data


def parse_data():
    return [d.split(',') for d in input_data.split('\n')]


def get_locations(data_line):
    locations = []

    for d in data_line:
        direction = d[0]
        steps = int(d[1:])

        x, y = locations[-1] if len(locations) > 0 else (0, 0)

        if direction == 'R':
            locations += ((x + i + 1, y) for i in range(steps))
        elif direction == 'L':
            locations += ((x - i - 1, y) for i in range(steps))
        elif direction == 'D':
            locations += ((x, y - i - 1) for i in range(steps))
        elif direction == 'U':
            locations += ((x, y + i + 1) for i in range(steps))
        else:
            raise Exception()

    return locations


def solve_a(data):
    locations_1 = get_locations(data[0])
    locations_2 = get_locations(data[1])

    locations_1_set = set(locations_1)

    intersection_1_2 = locations_1_set.intersection(locations_2)
    return min(map(lambda x: abs(x[0]) + abs(x[1]), intersection_1_2))


def solve_b(data):
    locations_1 = get_locations(data[0])
    locations_2 = get_locations(data[1])

    locations_1_set = set(locations_1)

    intersection_1_2 = locations_1_set.intersection(locations_2)
    return min(map(lambda x: locations_1.index(x) + locations_2.index(x) + 2, intersection_1_2))


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))