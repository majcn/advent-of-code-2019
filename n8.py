from aocd import data as input_data


def parse_data():
    return list(input_data)


def get_layers(data, image_size):
    nr_layers = len(data) // image_size

    return [[int(data[t + n * image_size]) for t in range(image_size)] for n in range(nr_layers)]


def solve_a(data):
    wide = 25
    tall = 6
    image_size = wide * tall

    layers = get_layers(data, image_size)
    layers_zeros = [[l, len(list(filter(lambda x: x == 0, l)))] for l in layers]
    layer = min(layers_zeros, key=lambda x: x[1])[0]

    return len(list(filter(lambda x: x == 1, layer))) * len(list(filter(lambda x: x == 2, layer)))


def solve_b(data):
    wide = 25
    tall = 6
    image_size = wide * tall

    layers = get_layers(data, image_size)
    image = [next(l[i] for l in layers if l[i] == 0 or l[i] == 1) for i in range(image_size)]

    s = '\n'
    for i in range(tall):
        for j in range(wide):
            s += '█' if image[j + i * wide] == 1 else ' '
        s += '\n'
    return s.rstrip()


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
