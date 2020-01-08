from aocd import data as input_data
import math


def parse_data():
    result = []
    for i, line in enumerate(input_data.split('\n')):
        result += [(j, -i) for j, d in enumerate(line) if d == '#']
    return result


def angle(x1, y1, x2, y2):
    cx = x2 - x1
    cy = y2 - y1
    acx = abs(cx)
    acy = abs(cy)

    if cx == 0 and cy > 0:
        return 0
    if cx == 0 and cy < 0:
        return 180
    if cx > 0 and cy == 0:
        return 90
    if cx < 0 and cy == 0:
        return 270
    if cx > 0 and cy > 0:
        return 90 - math.degrees(math.atan(acy / acx))
    if cx > 0 and cy < 0:
        return 90 + math.degrees(math.atan(acy / acx))
    if cx < 0 and cy < 0:
        return 270 - math.degrees(math.atan(acy / acx))
    if cx < 0 and cy > 0:
        return 270 + math.degrees(math.atan(acy / acx))


def best_location(data):
    result = [data[0], 0]
    for d1 in data:
        s = set()
        for d2 in data:
            if d1 == d2:
                continue

            s.add(angle(d1[0], d1[1], d2[0], d2[1]))
        if len(s) > result[1]:
            result = [d1, len(s)]
    return result


def solve_a(data):
    return best_location(data)[1]


def solve_b(data):
    asteroid_location = best_location(data)[0]

    result = []
    for d in data:
        if d == asteroid_location:
            continue

        d_distance = abs(d[0] - asteroid_location[0]) + abs(d[1] - asteroid_location[1])
        d_angle = angle(asteroid_location[0], asteroid_location[1], d[0], d[1])
        result.append([d_angle, d_distance, d])

    result.sort()

    prev_a = 0
    counter = 0
    for r in result:
        if r[0] == prev_a:
            r[0] += 360 * counter
            counter += 1
        else:
            prev_a = r[0]
            counter = 1

    result.sort()

    destroyed_200 = result[199][2]
    return abs(destroyed_200[0]) * 100 + abs(destroyed_200[1])


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
