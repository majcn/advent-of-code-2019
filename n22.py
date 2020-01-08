from aocd import data as input_data


def parse_data():
    result = []
    for line in input_data.split('\n'):
        if line.startswith('deal with increment'):
            result.append(('deal_with_increment', int(line.split(' ')[3])))

        if line.startswith('cut'):
            result.append(('cut', int(line.split(' ')[1])))

        if line.startswith('deal into new stack'):
            result.append(('deal_into_new_stack', None))

    return result


def solve_a(data):
    def deal_into_new_stack(cards):
        return list(cards[::-1])

    def cut(cards, N):
        return list(cards[N:]) + list(cards[:N])

    def deal_with_increment(cards, N):
        result = [0 for i in range(len(cards))]
        location = 0
        for i in range(len(cards)):
            result[location] = cards[i]
            location = (location + N) % len(cards)
        return result

    def f(i):
        r = i
        for instruction in data:
            if instruction[0] == 'deal_with_increment':
                r = deal_with_increment(r, instruction[1])
            elif instruction[0] == 'cut':
                r = cut(r, instruction[1])
            elif instruction[0] == 'deal_into_new_stack':
                r = deal_into_new_stack(r)
        return r

    return f(range(10007)).index(2019)


def solve_b(data):
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = egcd(b % a, a)
            return g, x - (b // a) * y, y

    def modinv(a, m):
        while a < 0:
            a = a + m

        g, x, y = egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def reverse_deal_into_new_stack(i):
        return (-i - 1) % D

    def reverse_cut(i, N):
        return (i + N) % D

    def reverse_deal_with_increment(i, N):
        return (modinv(N, D) * i) % D

    def f(i):
        r = i
        for instruction in data[::-1]:
            if instruction[0] == 'deal_with_increment':
                r = reverse_deal_with_increment(r, instruction[1])
            elif instruction[0] == 'cut':
                r = reverse_cut(r, instruction[1])
            elif instruction[0] == 'deal_into_new_stack':
                r = reverse_deal_into_new_stack(r)
        return r

    D = 119315717514047
    n = 101741582076661
    X = 2020

    Y = f(X)
    Z = f(Y)
    A = (Y - Z) * modinv(X - Y, D) % D
    B = (Y - A * X) % D

    return (pow(A, n, D) * X + (1 - pow(A, n, D)) * modinv(1 - A, D) * B) % D


print("Part 1: {}".format(solve_a(parse_data())))
print("Part 2: {}".format(solve_b(parse_data())))
