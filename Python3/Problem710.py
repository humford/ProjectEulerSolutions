import time


MODULUS = 1_000_000


def recurrenceNext(values, index, modulus=None):
    value = (
        values[index - 1]
        + 2 * values[index - 2]
        - 2 * values[index - 3]
        - values[index - 4]
        + values[index - 5]
        + values[index - 6]
        - values[index - 7]
    )

    if modulus is not None:
        value %= modulus
    return value


def twopalCount(total):
    a = [1, 1, 1, 2, 2, 3, 4]
    for n in range(7, total + 1):
        a.append(recurrenceNext(a, n))
    return (1 << (total // 2)) - a[total]


def firstDivisibleTwopalIndex():
    a = [1, 1, 1, 2, 2, 3, 4]
    power = pow(2, 3, MODULUS)
    n = 6

    while True:
        n += 1
        if n % 2 == 0:
            power = (2 * power) % MODULUS

        a.append(recurrenceNext(a, n, MODULUS))
        if n > 42 and (power - a[n]) % MODULUS == 0:
            return n


def runTests():
    assert twopalCount(6) == 4
    assert twopalCount(20) == 824
    assert twopalCount(42) == 1_999_923


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = firstDivisibleTwopalIndex()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
