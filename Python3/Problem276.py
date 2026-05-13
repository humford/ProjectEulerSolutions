import math
import time
from array import array


LIMIT = 10**7
REMAINDER_PREFIX = (0, 3, 7, 14, 14, 21, 25)


def partitionCountWithThreePartsUpTo(limit):
    count = limit + 1
    full_blocks, remainder = divmod(count, 6)
    remainder_sum = full_blocks * 25 + REMAINDER_PREFIX[remainder]
    square_sum = limit * (limit + 1) * (2 * limit + 1) // 6

    return (square_sum + 3 * count - remainder_sum) // 12


def triangleCount(limit):
    even_slack = partitionCountWithThreePartsUpTo(limit // 2)
    odd_slack = partitionCountWithThreePartsUpTo((limit + 3) // 2)

    return even_slack + odd_slack


def mobiusValues(limit):
    mobius = array("b", [0]) * (limit + 1)
    composite = bytearray(limit + 1)
    primes = []
    mobius[1] = 1

    for number in range(2, limit + 1):
        if composite[number] == 0:
            primes.append(number)
            mobius[number] = -1

        for prime in primes:
            value = number * prime
            if value > limit:
                break

            composite[value] = 1
            if number % prime == 0:
                mobius[value] = 0
                break

            mobius[value] = -mobius[number]

    return mobius


def primitiveTriangleCount(limit):
    mobius = mobiusValues(limit)
    total = 0

    for divisor in range(1, limit + 1):
        value = mobius[divisor]
        if value:
            total += value * triangleCount(limit // divisor)

    return total


def brutePrimitiveTriangleCount(limit):
    total = 0

    for a in range(1, limit + 1):
        for b in range(a, limit + 1):
            for c in range(b, limit + 1):
                if a + b + c > limit:
                    break
                if a + b > c and math.gcd(a, math.gcd(b, c)) == 1:
                    total += 1

    return total


def runTests():
    assert partitionCountWithThreePartsUpTo(6) == 7
    assert triangleCount(10) == 11
    assert primitiveTriangleCount(10) == 8
    assert primitiveTriangleCount(50) == brutePrimitiveTriangleCount(50)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primitiveTriangleCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
