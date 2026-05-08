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


def ceilingSquareRoot(number):
    root = math.isqrt(number)
    if root * root == number:
        return root
    return root + 1


def boundsForX(x, perimeter_limit):
    lower = x + ceilingSquareRoot(2 * x * x - 1)
    while lower * lower - 2 * x * lower - x * x + 1 < 0:
        lower += 1

    discriminant = x * x + 4 * (perimeter_limit * x - 1)
    upper = (-x + math.isqrt(discriminant)) // 2
    while upper * upper + x * upper + 1 - perimeter_limit * x > 0:
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


def tonelli(n, prime):
    if prime % 4 == 3:
        return pow(n, (prime + 1) // 4, prime)

    q = prime - 1
    shifts = 0
    while q % 2 == 0:
        shifts += 1
        q //= 2

    z = 2
    while pow(z, (prime - 1) // 2, prime) != prime - 1:
        z += 1

    m = shifts
    c = pow(z, q, prime)
    t = pow(n, q, prime)
    root = pow(n, (q + 1) // 2, prime)

    while t != 1:
        i = 1
        t2 = (t * t) % prime
        while t2 != 1:
            t2 = (t2 * t2) % prime
            i += 1

        b = pow(c, 1 << (m - i - 1), prime)
        m = i
        c = (b * b) % prime
        t = (t * c) % prime
        root = (root * b) % prime

    return root


def minusOneRootsPrimePower(prime, exponent, prime_power, cache):
    key = (prime, exponent)
    if key in cache:
        return cache[key]

    if prime == 2:
        roots = [1] if exponent == 1 else []
        cache[key] = roots
        return roots

    if prime % 4 != 1:
        cache[key] = []
        return []

    root = tonelli(prime - 1, prime)
    modulus = prime
    for _ in range(1, exponent):
        correction = -((root * root + 1) // modulus) * pow(2 * root, -1, prime)
        root += (correction % prime) * modulus
        modulus *= prime

    roots = [root % prime_power, (-root) % prime_power]
    cache[key] = roots
    return roots


def minusOneRootsMod(number, spf, cache):
    if number == 1:
        return [0]

    roots = [0]
    modulus = 1

    for prime, exponent, prime_power in factorPrimePowers(number, spf):
        local_roots = minusOneRootsPrimePower(prime, exponent, prime_power, cache)
        if not local_roots:
            return []

        inverse = pow(modulus, -1, prime_power)
        next_roots = []
        for existing_root in roots:
            for root in local_roots:
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


def barelyObtuseCount(perimeter_limit):
    total = 0
    max_x = maximumX(perimeter_limit)
    spf = smallestPrimeFactors(max_x)
    root_cache = {}

    for x in range(1, max_x + 1):
        lower, upper = boundsForX(x, perimeter_limit)
        if lower > upper:
            continue

        modulus = 2 * x
        for root in minusOneRootsMod(x, spf, root_cache):
            for residue in (root, root + x):
                representative = modulus if residue == 0 else residue
                y = (representative * representative + 1) // x
                if (x + y) % 2 == 0:
                    total += progressionCount(lower, upper, residue % modulus, modulus)

    return total


def runTests():
    assert barelyObtuseCount(100) == 6


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = barelyObtuseCount(75000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
