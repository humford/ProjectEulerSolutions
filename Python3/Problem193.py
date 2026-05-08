import math
import time
from array import array


def mobiusValues(limit):
    mobius = array("b", [0]) * (limit + 1)
    is_composite = bytearray(limit + 1)
    primes = []
    mobius[1] = 1

    for number in range(2, limit + 1):
        if not is_composite[number]:
            primes.append(number)
            mobius[number] = -1

        for prime in primes:
            multiple = number * prime
            if multiple > limit:
                break

            is_composite[multiple] = 1
            if number % prime == 0:
                mobius[multiple] = 0
                break

            mobius[multiple] = -mobius[number]

    return mobius


def squarefreeBelow(limit):
    root = math.isqrt(limit - 1)
    mobius = mobiusValues(root)
    maximum = limit - 1

    return sum(mobius[number] * (maximum // (number * number)) for number in range(1, root + 1))


def runTests():
    assert squarefreeBelow(10) == 6


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squarefreeBelow(2 ** 50)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
