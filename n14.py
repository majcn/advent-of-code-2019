from aocd import data as input_data
import math


def parse_data():
    result = {}
    for line in input_data.split("\n"):
        l, r = line.split(" => ")
        fr = tuple(r.split(" "))

        p1 = [x.split(" ") for x in l.split(", ")]
        p1 = [(int(x[0]), x[1]) for x in p1]
        p2 = int(fr[0])

        result[fr[1]] = (p1, p2)

    return result


def shop(data, item_name, item_count, my_items):
    supply = my_items[item_name]
    if supply >= item_count:
        return True

    if item_name == 'ORE':
        return False

    requirements, result_count = data[item_name]
    multiplier = math.ceil((item_count - supply) / result_count)
    for r_count, r_name in requirements:
        r_needed = r_count * multiplier
        s_successful = shop(data, r_name, r_needed, my_items)
        if not s_successful:
            return False

        my_items[r_name] -= multiplier * r_count
    my_items[item_name] += multiplier * result_count

    return True


def solve_a(data):
    start_ore = 1000000000000
    my_items = {i: 0 for i in data}
    my_items['ORE'] = start_ore

    shop(data, 'FUEL', 1, my_items)
    return start_ore - my_items['ORE']


def solve_b(data):
    start_ore = 1000000000000
    c_min = 1
    c_max = start_ore
    c = (c_max + c_min) // 2
    while True:
        my_items = {i: 0 for i in data}
        my_items['ORE'] = start_ore

        s_successful = shop(data, 'FUEL', c, my_items)

        if s_successful:
            c_min = c + 1
        else:
            c_max = c - 1

        tmp = (c_max + c_min) // 2
        if tmp == c:
            break
        c = tmp
    return c


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
