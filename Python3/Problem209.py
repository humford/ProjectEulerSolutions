import time


def lucasNumbers(limit):
    values = [0] * (limit + 1)
    values[0] = 2
    values[1] = 1

    for index in range(2, limit + 1):
        values[index] = values[index - 1] + values[index - 2]

    return values


def nextState(state):
    bits = [(state >> index) & 1 for index in range(6)]
    a, b, c, d, e, f = bits
    next_bits = [b, c, d, e, f, a ^ (b & c)]

    result = 0
    for index, bit in enumerate(next_bits):
        result |= bit << index

    return result


def truthTableCount():
    connections = [nextState(state) for state in range(64)]
    lucas = lucasNumbers(64)
    seen = [False] * 64
    result = 1

    for start in range(64):
        if seen[start]:
            continue

        current = start
        cycle_length = 0
        while not seen[current]:
            seen[current] = True
            cycle_length += 1
            current = connections[current]

        result *= lucas[cycle_length]

    return result


def runTests():
    assert lucasNumbers(5)[:6] == [2, 1, 3, 4, 7, 11]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = truthTableCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
