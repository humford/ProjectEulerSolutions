import itertools
import time
from array import array


MODULUS = 135_707_531


def cycleDistance(flow):
    floorCount = len(flow)
    best = floorCount
    for order in itertools.permutations(range(floorCount)):
        cycle = [0] * floorCount
        for index, floor in enumerate(order):
            cycle[floor] = order[(index + 1) % floorCount]
        best = min(best, sum(cycle[floor] != flow[floor] for floor in range(floorCount)))
    return best


def bruteBlackoutRewiringSum(floors):
    total = 0
    for flow in itertools.product(range(floors), repeat=floors):
        if all(flow[floor] != floor for floor in range(floors)):
            total += cycleDistance(flow)
    return total


def modularInverses(limit):
    inverses = array("I", [0]) * (limit + 1)
    if limit >= 1:
        inverses[1] = 1
    for number in range(2, limit + 1):
        inverses[number] = (MODULUS - MODULUS // number) * inverses[MODULUS % number] % MODULUS
    return inverses


def blackoutRewiringSum(floors):
    if floors <= 2:
        return 0

    inverses = modularInverses(floors)

    factorial = 1
    for number in range(1, floors + 1):
        factorial = factorial * number % MODULUS

    # A loopless functional digraph needs one rewire for each missing target
    # plus one for each cycle component with no external incoming edge.  The
    # single full-cycle case is already valid, so that pure-cycle term cancels.
    total = floors * (floors - 1) % MODULUS
    total = total * pow(floors - 2, floors - 1, MODULUS) % MODULUS

    inverseFactorial = 1
    for outsideCount in range(2, floors - 1):
        inverseFactorial = inverseFactorial * inverses[outsideCount] % MODULUS
        cycleSize = floors - outsideCount
        term = factorial * inverses[cycleSize] % MODULUS
        term = term * inverseFactorial % MODULUS
        term = term * pow(outsideCount - 1, outsideCount, MODULUS) % MODULUS
        total = (total + term) % MODULUS

    return total


def runTests():
    assert bruteBlackoutRewiringSum(3) == 6
    assert blackoutRewiringSum(3) == 6
    assert blackoutRewiringSum(8) == 16_276_736
    assert blackoutRewiringSum(100) == 84_326_147


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = blackoutRewiringSum(12_344_321)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
