from itertools import permutations
from math import gcd
import time


HAND_SPEEDS = (1, 12, 720)
IDENTITY = (0, 1, 2)


def extendedGcd(a, b):
    if b == 0:
        return a, 1, 0

    divisor, x, y = extendedGcd(b, a % b)
    return divisor, y, x - (a // b) * y


def normalizedFraction(numerator, denominator):
    numerator %= denominator
    divisor = gcd(numerator, denominator)
    return numerator // divisor, denominator // divisor


def ambiguousTimes():
    times = set()

    for permutation in permutations(range(3)):
        if permutation == IDENTITY:
            continue

        a = HAND_SPEEDS[1] - HAND_SPEEDS[0]
        c = HAND_SPEEDS[2] - HAND_SPEEDS[0]
        b = -(HAND_SPEEDS[permutation[1]] - HAND_SPEEDS[permutation[0]])
        d = -(HAND_SPEEDS[permutation[2]] - HAND_SPEEDS[permutation[0]])
        determinant = a * d - b * c
        denominator = abs(determinant)

        divisor, alpha, beta = extendedGcd(a, c)
        assert divisor == 1
        uFactor = -(alpha * b + beta * d)

        for tNumerator in range(denominator):
            uNumerator = (uFactor * tNumerator) % denominator
            if uNumerator == tNumerator:
                continue

            times.add(normalizedFraction(tNumerator, denominator))

    return times


def isAmbiguous(numerator, denominator, times=None):
    if times is None:
        times = ambiguousTimes()
    return normalizedFraction(numerator, denominator) in times


def solve():
    return len(ambiguousTimes())


def runTests():
    times = ambiguousTimes()
    assert isAmbiguous(1, 8, times)
    assert isAmbiguous(5, 8, times)
    assert not isAmbiguous(0, 1, times)
    assert not isAmbiguous(1, 4, times)
    assert not isAmbiguous(3, 4, times)
    assert len(times) == 1541414


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
