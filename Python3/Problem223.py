import math
import time


def smallestPrimeFactors(limit):
    spf = list(range(limit + 1))
    spf[0] = 0
    spf[1] = 1

    for number in range(2, math.isqrt(limit) + 1):
        if spf[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if spf[multiple] == multiple:
                    spf[multiple] = number

    return spf


def boundsForX(x, perimeter_limit):
    lower = x + math.isqrt(2 * x * x + 1)
    while lower * lower - 2 * x * lower - x * x - 1 < 0:
        lower += 1

    discriminant = x * x + 4 * (perimeter_limit * x + 1)
    upper = (-x + math.isqrt(discriminant)) // 2
    while upper * upper + x * upper - (perimeter_limit * x + 1) > 0:
        upper -= 1

    return lower, upper


def maximumX(perimeter_limit):
    best = 0
    x = 1

    while True:
        lower, upper = boundsForX(x, perimeter_limit)
        if lower <= upper:
            best = x
        elif x > best + 1000:
            return best
        x += 1


def primePowerRoots(prime, exponent, prime_power):
    if prime == 2:
        if exponent == 1:
            return [1]
        if exponent == 2:
            return [1, 3]

        half = 1 << (exponent - 1)
        return [1, prime_power - 1, 1 + half, half - 1]

    return [1, prime_power - 1]


def factorPrimePowers(number, spf):
    factors = []

    while number > 1:
        prime = spf[number]
        exponent = 0
        prime_power = 1
        while number % prime == 0:
            number //= prime
            exponent += 1
            prime_power *= prime
        factors.append((prime, exponent, prime_power))

    return factors


def squareOneRootsMod(number, spf):
    if number == 1:
        return [0]

    roots = [0]
    modulus = 1

    for prime, exponent, prime_power in factorPrimePowers(number, spf):
        next_roots = []
        inverse = pow(modulus, -1, prime_power)

        for existing_root in roots:
            for root in primePowerRoots(prime, exponent, prime_power):
                combined = existing_root + modulus * (
                    ((root - existing_root) * inverse) % prime_power
                )
                next_roots.append(combined % (modulus * prime_power))

        roots = next_roots
        modulus *= prime_power

    return roots


def progressionCount(lower, upper, residue, modulus):
    first = modulus if residue == 0 else residue
    if first < lower:
        first += ((lower - first + modulus - 1) // modulus) * modulus

    if first > upper:
        return 0
    return (upper - first) // modulus + 1


def barelyAcuteCount(perimeter_limit):
    total = (perimeter_limit - 1) // 2
    max_x = maximumX(perimeter_limit)
    spf = smallestPrimeFactors(max_x)

    for x in range(1, max_x + 1):
        lower, upper = boundsForX(x, perimeter_limit)
        if lower > upper:
            continue

        modulus = 2 * x
        for root in squareOneRootsMod(x, spf):
            for residue in (root, root + x):
                representative = modulus if residue == 0 else residue
                y = (representative * representative - 1) // x
                if (x + y) % 2 == 0:
                    total += progressionCount(lower, upper, residue % modulus, modulus)

    return total


def runTests():
    assert barelyAcuteCount(10000) == 13656


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = barelyAcuteCount(25000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
