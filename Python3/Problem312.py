import time


MODULUS = 13**8


def cycleCount(n, modulus=None):
    if n in (1, 2):
        return 1
    if n == 3:
        return 8

    if modulus is None:
        exponent = (3 ** (n - 2) - 3) // 2
    else:
        exponent_modulus = 4 * 13 ** 7 if modulus == MODULUS else 2 * modulus
        exponent = (pow(3, n - 2, exponent_modulus) - 3) // 2

    return 8 * pow(12, exponent, modulus) % modulus if modulus else 8 * 12**exponent


def nestedCycleCount():
    first = cycleCount(10000 % (6 * 13**2), 6 * 13**4)
    second = cycleCount(first, 6 * 13**6)
    return cycleCount(second, MODULUS)


def runTests():
    assert cycleCount(1) == 1
    assert cycleCount(2) == 1
    assert cycleCount(3) == 8
    assert cycleCount(5) == 71328803586048
    assert cycleCount(10000, 10**8) == 37652224
    assert cycleCount(10000, MODULUS) == 617720485


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nestedCycleCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
