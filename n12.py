from aocd import data as input_data
import re


def parse_data():
    re_prog = re.compile(r'^<x=(-?[\d]*), y=(-?[\d]*), z=(-?[\d]*)>$')
    return [tuple(map(int, re_prog.match(x).groups())) for x in input_data.split('\n')]


def solve_a(data):
    moons = [[[d[0], 0], [d[1], 0], [d[2], 0]] for d in data]

    for _ in range(1000):
        for m1 in moons:
            for m2 in moons:
                if m1 != m2:
                    for i in range(3):
                        if m1[i][0] < m2[i][0]:
                            m1[i][1] += 1
                        elif m1[i][0] > m2[i][0]:
                            m1[i][1] -= 1

        for m in moons:
            for i in range(3):
                m[i][0] += m[i][1]

    result = 0
    for m in moons:
        pot = 0
        kin = 0
        for i in range(3):
            pot += abs(m[i][0])
            kin += abs(m[i][1])
        result += pot * kin
    return result


def solve_b(data):
    moons = [[[d[0], 0], [d[1], 0], [d[2], 0]] for d in data]

    def gcd(a, b):
        while b != 0:
           t = b
           b = a % b
           a = t
        return a

    def lcm(a, b, c):
        lcm_ab = a * b // gcd(a, b)
        lcm_abc = lcm_ab * c // gcd(lcm_ab, c)

        return lcm_abc

    result = []
    for i in range(3):
        cache = set()
        while True:
            for m1 in moons:
                for m2 in moons:
                    if m1 != m2:
                        if m1[i][0] < m2[i][0]:
                            m1[i][1] += 1
                        elif m1[i][0] > m2[i][0]:
                            m1[i][1] -= 1

            for m in moons:
                m[i][0] += m[i][1]

            h_moons = tuple([tuple(m[i]) for m in moons])
            if h_moons in cache:
                break
            cache.add(h_moons)
        result.append(len(cache))

    return lcm(*result)


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
