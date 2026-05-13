import bisect
from decimal import Decimal, getcontext
import time


SHIFT = 180
MAX_POWER = SHIFT + 120
FIXED_PRECISION_BITS = 160


def realRoot():
    getcontext().prec = 100
    root = Decimal("1.4")
    for _ in range(80):
        root -= (root**3 - root**2 - 1) / (3 * root * root - 2 * root)
    return root


ROOT = realRoot()
REAL_ROOT = float(ROOT)
SCALE = 1 << FIXED_PRECISION_BITS
ROOT_FIXED = int(ROOT * SCALE)
ROOT_SQUARED_FIXED = int(ROOT * ROOT * SCALE)


def powerVectors(limit):
    vectors = [(0, 0, 0)] * (limit + 1)
    vectors[0] = (1, 0, 0)
    vectors[1] = (0, 1, 0)
    vectors[2] = (0, 0, 1)
    for index in range(3, limit + 1):
        previous = vectors[index - 1]
        back = vectors[index - 3]
        vectors[index] = (
            previous[0] + back[0],
            previous[1] + back[1],
            previous[2] + back[2],
        )
    return vectors


def realPowerApproximations(limit):
    values = [1.0] * (limit + 1)
    for index in range(1, limit + 1):
        values[index] = values[index - 1] * REAL_ROOT
    return values


POWER_VECTORS = powerVectors(MAX_POWER)
POWER_APPROXIMATIONS = realPowerApproximations(MAX_POWER)


def signOfAlgebraic(a, b, c):
    value = a * SCALE + b * ROOT_FIXED + c * ROOT_SQUARED_FIXED
    return (value > 0) - (value < 0)


def representationWeight(n):
    shiftedUnit = POWER_VECTORS[SHIFT]
    current0 = n * shiftedUnit[0]
    current1 = n * shiftedUnit[1]
    current2 = n * shiftedUnit[2]
    approximateValue = n * POWER_APPROXIMATIONS[SHIFT]
    lastPower = MAX_POWER + 3
    weight = 0

    while current0 or current1 or current2:
        high = min(lastPower - 3, MAX_POWER)
        power = bisect.bisect_right(
            POWER_APPROXIMATIONS, approximateValue, 0, high + 1
        ) - 1
        if power < 0:
            power = 0

        while power < high:
            trial = POWER_VECTORS[power + 1]
            if (
                signOfAlgebraic(
                    current0 - trial[0],
                    current1 - trial[1],
                    current2 - trial[2],
                )
                < 0
            ):
                break
            power += 1

        while True:
            trial = POWER_VECTORS[power]
            if (
                signOfAlgebraic(
                    current0 - trial[0],
                    current1 - trial[1],
                    current2 - trial[2],
                )
                >= 0
            ):
                break
            power -= 1
            if power < 0:
                raise RuntimeError("SHIFT is too small for this value")

        chosen = POWER_VECTORS[power]
        current0 -= chosen[0]
        current1 -= chosen[1]
        current2 -= chosen[2]
        approximateValue -= POWER_APPROXIMATIONS[power]
        lastPower = power
        weight += 1

    return weight


def squareRepresentationWeightSum(limit):
    return sum(representationWeight(n * n) for n in range(1, limit + 1))


def runTests():
    assert representationWeight(3) == 4
    assert representationWeight(10) == 3
    assert squareRepresentationWeightSum(10) == 61
    assert squareRepresentationWeightSum(1_000) == 19_403


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squareRepresentationWeightSum(5_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
