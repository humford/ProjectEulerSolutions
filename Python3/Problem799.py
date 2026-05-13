import math
import random
import time


MILLER_RABIN_BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def pentagonal(n):
    return n * (3 * n - 1) // 2


def isPrime64(n):
    if n < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % prime == 0:
            return n == prime

    d = n - 1
    shifts = 0
    while d % 2 == 0:
        shifts += 1
        d //= 2

    for base in MILLER_RABIN_BASES_64:
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(shifts - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollardRho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = random.randrange(1, n - 1)
        x = random.randrange(0, n)
        y = x
        divisor = 1

        while divisor == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            divisor = math.gcd(abs(x - y), n)

        if divisor != n:
            return divisor


def factorize(n):
    factors = {}
    stack = [n]

    while stack:
        value = stack.pop()
        if value == 1:
            continue
        if isPrime64(value):
            factors[value] = factors.get(value, 0) + 1
            continue

        divisor = pollardRho(value)
        stack.append(divisor)
        stack.append(value // divisor)

    return factors


SQRT_MINUS_ONE_CACHE = {}
CORNACCHIA_CACHE = {}


def sqrtMinusOneModPrime(prime):
    cached = SQRT_MINUS_ONE_CACHE.get(prime)
    if cached is not None:
        return cached

    for value in (2, 3, 5, 6, 7, 10, 11, 13, 17, 19, 23, 29):
        if value % prime and pow(value, (prime - 1) // 2, prime) == prime - 1:
            result = pow(value, (prime - 1) // 4, prime)
            SQRT_MINUS_ONE_CACHE[prime] = result
            return result

    value = 2
    while True:
        if pow(value, (prime - 1) // 2, prime) == prime - 1:
            result = pow(value, (prime - 1) // 4, prime)
            SQRT_MINUS_ONE_CACHE[prime] = result
            return result
        value += 1


def cornacchiaPrimeSumSquares(prime):
    cached = CORNACCHIA_CACHE.get(prime)
    if cached is not None:
        return cached

    root = sqrtMinusOneModPrime(prime)

    def run(value):
        r0, r1 = prime, value
        while r1 * r1 > prime:
            r0, r1 = r1, r0 % r1
        a = r1
        bSquared = prime - a * a
        b = math.isqrt(bSquared)
        if b * b != bSquared:
            raise ValueError
        return a, b

    try:
        result = run(root)
    except ValueError:
        result = run(prime - root)

    CORNACCHIA_CACHE[prime] = result
    return result


def gaussianMultiply(u, v, a, b):
    return u * a - v * b, u * b + v * a


def countPentagonalSumWays(m):
    x = 6 * m - 1
    N = x * x + 1
    factors = factorize(N)

    options = []
    for prime, exponent in factors.items():
        if prime == 2:
            continue

        a, b = cornacchiaPrimeSumSquares(prime)
        powers = [(1, 0)]
        conjugatePowers = [(1, 0)]
        for _ in range(exponent):
            powers.append(gaussianMultiply(powers[-1][0], powers[-1][1], a, b))
            conjugatePowers.append(gaussianMultiply(conjugatePowers[-1][0], conjugatePowers[-1][1], a, -b))

        local = []
        for k in range(exponent + 1):
            local.append(
                gaussianMultiply(
                    powers[k][0],
                    powers[k][1],
                    conjugatePowers[exponent - k][0],
                    conjugatePowers[exponent - k][1],
                )
            )
        options.append(local)

    representations = [(1, 0)]
    for local in options:
        nextRepresentations = []
        for u, v in representations:
            for a, b in local:
                nextRepresentations.append(gaussianMultiply(u, v, a, b))
        representations = nextRepresentations

    seen = set()
    for u, v in representations:
        u, v = gaussianMultiply(u, v, 1, 1)
        u = abs(u)
        v = abs(v)
        if u == 0 or v == 0:
            continue
        if u > v:
            u, v = v, u
        if u % 3 == 2 and v % 3 == 2:
            seen.add((u, v))

    return len(seen)


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for n in range(2, math.isqrt(limit) + 1):
        if sieve[n]:
            sieve[n * n:limit + 1:n] = b"\x00" * (((limit - n * n) // n) + 1)
    return [n for n in range(limit + 1) if sieve[n]]


def nextPrimeAfter(n):
    candidate = n + 1
    if candidate % 2 == 0:
        candidate += 1
    while not isPrime64(candidate):
        candidate += 2
    return candidate


def precomputeRoots(limit):
    roots = []
    for prime in primesUpTo(limit):
        if prime % 4 != 1:
            continue
        sqrtMinusOne = sqrtMinusOneModPrime(prime)
        inverse6 = pow(6, prime - 2, prime)
        roots.append((prime, ((1 + sqrtMinusOne) * inverse6) % prime, ((1 - sqrtMinusOne) * inverse6) % prime))
    return roots, nextPrimeAfter(limit)


def upperFactorMultiplier(remainder, minPrime):
    if remainder <= 1:
        return 1
    return 1 << int(math.log(remainder, minPrime))


def findAnswer(blockSize=50_000, primeLimit=200_000):
    roots, nextPrime = precomputeRoots(primeLimit)
    startM = 1

    while True:
        residuals = [0] * blockSize
        divisorProducts = [1] * blockSize

        x = 6 * startM - 1
        N = x * x + 1
        for i in range(blockSize):
            residuals[i] = N // 2
            x += 6
            N = x * x + 1

        for prime, root1, root2 in roots:
            startMod = startM % prime
            for root in (root1, root2):
                index = (root - startMod) % prime
                while index < blockSize:
                    value = residuals[index]
                    if value % prime == 0:
                        exponent = 0
                        while value % prime == 0:
                            value //= prime
                            exponent += 1
                        residuals[index] = value
                        divisorProducts[index] *= exponent + 1
                    index += prime

        for i in range(blockSize):
            if divisorProducts[i] * upperFactorMultiplier(residuals[i], nextPrime) < 202:
                continue

            m = startM + i
            if countPentagonalSumWays(m) > 100:
                return pentagonal(m)

        startM += blockSize


def runTests():
    random.seed(0)
    assert countPentagonalSumWays(8) == 1
    assert countPentagonalSumWays(49) == 2
    assert countPentagonalSumWays(268) == 3


if __name__ == "__main__":
    random.seed(0)
    runTests()
    start = time.time()
    answer = findAnswer()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
