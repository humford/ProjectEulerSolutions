import time


MODULUS = 900_497_239
TARGET_N = 10_000


def nextPowerOfTwoStrictlyGreater(n):
    return 1 << n.bit_length()


def t(n):
    modulus = nextPowerOfTwoStrictlyGreater(n)
    return (-n * n - (n & 1)) % modulus


def exactSValues(maxN):
    values = [0] * (maxN + 1)
    total = 0
    nextLimit = 2
    index = 1

    for n in range(1, (1 << maxN) + 1):
        total += t(n)
        if n == nextLimit:
            values[index] = total
            index += 1
            nextLimit <<= 1
            if index > maxN:
                break

    return values


def recurrenceNext(values):
    return (
        7 * values[-1]
        - 6 * values[-2]
        - 48 * values[-3]
        + 112 * values[-4]
        - 64 * values[-5]
    )


def SMod(N, modulus=MODULUS):
    exact = exactSValues(15)

    for index in range(6, 16):
        assert exact[index] == recurrenceNext(exact[index - 5:index])

    if N <= 15:
        return exact[N] % modulus

    window = [value % modulus for value in exact[1:6]]
    for _ in range(6, N + 1):
        window.append(recurrenceNext(window) % modulus)
        window.pop(0)

    return window[-1]


def solve():
    return SMod(TARGET_N)


def runTests():
    assert t(1) == 0
    assert t(2) == 0
    assert t(3) == 2
    assert exactSValues(10)[10] == 361522
    assert solve() == 646900900


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
