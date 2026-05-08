import time


def factorization(number):
    factors = []
    factor = 2
    remaining = number

    while factor * factor <= remaining:
        if remaining % factor == 0:
            exponent = 0
            while remaining % factor == 0:
                remaining //= factor
                exponent += 1
            factors.append((factor, exponent))
        factor += 1 if factor == 2 else 2

    if remaining > 1:
        factors.append((remaining, 1))

    return factors


def phiFromFactors(number, factors):
    result = number
    for prime, _ in factors:
        result -= result // prime
    return result


def laserBeamCount(reflections):
    if reflections % 2 == 0:
        return 0

    m = (reflections + 3) // 2
    if m % 3 == 0:
        return 0

    factors = factorization(m)
    result = phiFromFactors(m, factors)

    if all(prime % 3 != 1 for prime, _ in factors):
        correction = -1 if m % 3 == 2 else 1
        result -= correction * (2 ** len(factors))

    return result // 3


def runTests():
    assert laserBeamCount(11) == 2
    assert laserBeamCount(1000001) == 80840


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = laserBeamCount(12017639147)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
