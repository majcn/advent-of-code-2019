from aocd import data as input_data


def parse_data():
    return [int(d) for d in input_data.split('-')]


def solve_a(data):
    result = 0
    for x in range(data[0], data[1]):
        cx = str(x)
        is_valid = False
        for i in range(len(cx) - 1):
            if cx[i] > cx[i + 1]:
                is_valid = False
                break
            if cx[i] == cx[i + 1]:
                is_valid = True
        if is_valid:
            result += 1

    return result


def solve_b(data):
    part_a_result = []
    for x in range(data[0], data[1]):
        cx = str(x)
        is_valid = False
        for i in range(len(cx) - 1):
            if cx[i] > cx[i + 1]:
                is_valid = False
                break
            if cx[i] == cx[i + 1]:
                is_valid = True
        if is_valid:
            part_a_result.append(cx)

    result = 0
    for cx in part_a_result:
        counter = {c: 1 for c in cx}
        for i in range(len(cx) - 1):
            if cx[i] == cx[i + 1]:
                counter[cx[i]] += 1
        if 2 in counter.values():
            result += 1

    return result


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
