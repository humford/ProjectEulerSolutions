import time
from array import array


PROBLEM_LIMIT = 20_000_000


def smallestPrimeFactors(limit):
    factors = array("I", range(limit + 1))

    for number in range(2, int(limit**0.5) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number

    return factors


def primePowerRoots(prime, primePower):
    if prime != 2:
        return (1, primePower - 1)

    if primePower == 2:
        return (1,)
    if primePower == 4:
        return (1, 3)

    half = primePower // 2
    return (1, primePower - 1, 1 + half, half - 1)


def factorPrimePowers(number, factors):
    while number > 1:
        prime = factors[number]
        primePower = 1

        while number % prime == 0:
            number //= prime
            primePower *= prime

        yield prime, primePower


def selfInverseRoots(modulus, factors):
    roots = [(0, 1)]

    # x^2 == 1 modulo each prime power factor; combine those local roots
    # with CRT to get all roots modulo n.
    for prime, primePower in factorPrimePowers(modulus, factors):
        nextRoots = []
        options = primePowerRoots(prime, primePower)

        for residue, currentModulus in roots:
            inverse = pow(currentModulus, -1, primePower)

            for targetResidue in options:
                multiplier = (targetResidue - residue) * inverse % primePower
                nextRoots.append(
                    (
                        residue + currentModulus * multiplier,
                        currentModulus * primePower,
                    )
                )

        roots = nextRoots

    return [residue for residue, _ in roots]


def largestSelfInverse(modulus, factors=None):
    if factors is None:
        factors = smallestPrimeFactors(modulus)

    best = 1
    excludedRoot = modulus - 1

    for root in selfInverseRoots(modulus, factors):
        if root != excludedRoot and root > best:
            best = root

    return best


def inverseSum(limit=PROBLEM_LIMIT):
    factors = smallestPrimeFactors(limit)
    total = 0

    for modulus in range(3, limit + 1):
        total += largestSelfInverse(modulus, factors)

    return total


def runTests():
    factors = smallestPrimeFactors(100)
    assert largestSelfInverse(7, factors) == 1
    assert largestSelfInverse(15, factors) == 11
    assert largestSelfInverse(100, factors) == 51


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = inverseSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
