from math import gcd, isqrt
import time


TARGET = 1_000_000


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for prime in range(2, isqrt(limit) + 1):
        if isPrime[prime]:
            start = prime * prime
            isPrime[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )

    return [value for value in range(2, limit + 1) if isPrime[value]]


PRIMES = primeSieve(10**6)


def factorization(value):
    factors = []
    reduced = value

    for prime in PRIMES:
        if prime * prime > reduced:
            break
        if reduced % prime == 0:
            exponent = 0
            while reduced % prime == 0:
                reduced //= prime
                exponent += 1
            factors.append((prime, exponent))
        if reduced == 1:
            break

    if reduced > 1:
        factors.append((reduced, 1))

    return factors


def divisorsFromFactors(factors):
    divisors = [1]
    for prime, exponent in factors:
        nextDivisors = []
        power = 1
        for _ in range(exponent + 1):
            for divisor in divisors:
                nextDivisors.append(divisor * power)
            power *= prime
        divisors = nextDivisors
    return divisors


def uCandidatesFromZFactors(factors):
    candidates = []
    primes = [prime for prime, _ in factors]
    exponentLimits = [2 * exponent // 3 for _, exponent in factors]

    def visit(index, current):
        if index == len(primes):
            candidates.append(current)
            return

        prime = primes[index]
        value = 1
        for _ in range(exponentLimits[index] + 1):
            visit(index + 1, current * value)
            value *= prime

    visit(0, 1)
    return candidates


def integerCubeRoot(value):
    root = int(round(value ** (1.0 / 3.0)))
    while (root + 1) ** 3 <= value:
        root += 1
    while root**3 > value:
        root -= 1
    return root


def countTriangles(limit):
    total = 0

    for z in range(1, limit // 3 + 1):
        zFactors = factorization(z)
        zSquared = z * z

        for u in uCandidatesFromZFactors(zFactors):
            uCubed = u * u * u
            if zSquared % uCubed != 0:
                continue

            w = zSquared // uCubed
            vMaximum = integerCubeRoot((limit * limit) // w)

            if vMaximum < u:
                continue

            for v in range(u, vMaximum + 1):
                if gcd(u, v) != 1:
                    continue

                product = v * w
                divisorPairs = divisorsFromFactors(factorization(product))
                sideScaleSum = u + v

                for p in divisorPairs:
                    q = product // p
                    if p <= q:
                        continue
                    if (p ^ q) & 1:
                        continue

                    g = (p + q) // 2
                    m = (p - q) // 2
                    if m <= 0 or g <= m:
                        continue

                    a = g * u
                    b = g * v
                    c = m * sideScaleSum
                    perimeter = a + b + c

                    if perimeter > limit:
                        continue
                    if a <= b <= c and a + b > c:
                        total += 1

    return total


def bruteCount(limit):
    total = 0

    for a in range(1, limit // 3 + 1):
        for b in range(a, (limit - a) // 2 + 1):
            maximumC = min(a + b - 1, limit - a - b)
            for c in range(b, maximumC + 1):
                numerator = a**3 * (a + b + c) * (a + b - c)
                denominator = b * (a + b) ** 2
                if numerator % denominator:
                    continue
                ceSquared = numerator // denominator
                ce = isqrt(ceSquared)
                if ce * ce == ceSquared:
                    total += 1

    return total


def solve():
    return countTriangles(TARGET)


def runTests():
    for limit in (60, 80, 100, 150, 200):
        assert countTriangles(limit) == bruteCount(limit)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
