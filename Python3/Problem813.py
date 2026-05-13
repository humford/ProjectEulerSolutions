import time


MOD = 1_000_000_007


def xorProduct(a, b):
    result = 0
    shift = 0

    while b:
        if b & 1:
            result ^= a << shift
        b >>= 1
        shift += 1

    return result


def xorPower(base, exponent):
    result = 1

    while exponent:
        if exponent & 1:
            result = xorProduct(result, base)
        base = xorProduct(base, base)
        exponent >>= 1

    return result


def degreesForPowerOfEleven(exponent):
    degrees = {0}
    bitValue = 1

    while exponent:
        if exponent & 1:
            nextDegrees = set()
            for degree in degrees:
                for add in (0, bitValue, 3 * bitValue):
                    nextDegree = degree + add
                    if nextDegree in nextDegrees:
                        nextDegrees.remove(nextDegree)
                    else:
                        nextDegrees.add(nextDegree)
            degrees = nextDegrees

        exponent >>= 1
        bitValue <<= 1

    return degrees


def PMod(exponent, modulus=MOD):
    total = 0
    for degree in degreesForPowerOfEleven(exponent):
        total = (total + pow(2, degree, modulus)) % modulus
    return total


def solve():
    exponent = 8 ** 12 * 12 ** 8
    return PMod(exponent)


def runTests():
    assert xorProduct(11, 11) == 69
    assert xorPower(11, 2) == 69


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
