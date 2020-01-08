from aocd import data as input_data


def parse_data():
    return [int(x) for x in input_data]


def solve_a(data):
    signal = data
    signal_len = len(data)

    pattern = [0, 1, 0, -1]
    patterns = [[pattern[((x + 1) // (i + 1)) % 4] for x in range(signal_len)] for i in range(signal_len)]

    for i in range(100):
        signal = [abs(sum(signal[x] * patterns[i][x] for x in range(signal_len))) % 10 for i in range(signal_len)]

    return ''.join(map(str, signal[:8]))


def solve_b(data):
    offset = int(''.join(map(str, data[:7])))

    signal = [int(x) for x in data] * 10000

    x = signal[offset:]
    for _ in range(100):
        prev = 0
        for i in range(len(x)):
            loc = -i-1

            r = prev + x[loc]
            prev = r

            x[loc] = abs(r) % 10

    return ''.join(map(str, x[:8]))


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
