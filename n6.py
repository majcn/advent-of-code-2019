from aocd import data as input_data


def parse_data():
    return [d.split(')') for d in input_data.split('\n')]


def path(start, end, graph):
    result = []

    e = start
    result.append(e)
    while e != end:
        e = graph[e]
        result.append(e)

    return result


def solve_a(data):
    graph = {d[1]: d[0] for d in data}

    return sum(len(path(x, 'COM', graph)) - 1 for x in graph)


def solve_b(data):
    graph = {d[1]: d[0] for d in data}

    san = path('SAN', 'COM', graph)
    you = path('YOU', 'COM', graph)

    return min(i + j - 2 for i in range(len(san)) for j in range(len(you)) if san[i] == you[j])


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
