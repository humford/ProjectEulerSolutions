import math
import time


MOD = 993_353_399
MILLER_RABIN_BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
RNG_STATE = 0x9E3779B97F4A7C15


def sievePrimes(limit):
    if limit < 2:
        return []
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"
    for n in range(2, math.isqrt(limit) + 1):
        if isPrime[n]:
            isPrime[n * n:limit + 1:n] = b"\x00" * (((limit - n * n) // n) + 1)
    return [n for n in range(2, limit + 1) if isPrime[n]]


TRIAL_PRIMES_10K = sievePrimes(10_000)


def isPrime64(n):
    if n < 2:
        return False
    for prime in SMALL_PRIMES:
        if n == prime:
            return True
        if n % prime == 0:
            return False

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


def rand64():
    global RNG_STATE
    x = RNG_STATE & ((1 << 64) - 1)
    x ^= x >> 12
    x ^= (x << 25) & ((1 << 64) - 1)
    x ^= x >> 27
    RNG_STATE = x
    return (x * 2_685_821_657_736_338_717) & ((1 << 64) - 1)


def pollardRho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = rand64() % (n - 1) + 1
        x = rand64() % (n - 2) + 2
        y = x
        divisor = 1

        while divisor == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            divisor = math.gcd(abs(x - y), n)

        if divisor != n:
            return divisor


def factorize64(n):
    factors = {}

    for prime in TRIAL_PRIMES_10K:
        if prime * prime > n:
            break
        if n % prime == 0:
            exponent = 0
            while n % prime == 0:
                n //= prime
                exponent += 1
            factors[prime] = factors.get(prime, 0) + exponent

    if n == 1:
        return factors
    if isPrime64(n):
        factors[n] = factors.get(n, 0) + 1
        return factors

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


def gPrimePower(q, exponent, modulus=None):
    if modulus is None:
        total = 0
        for t in range(1, exponent + 1):
            total += t * t * q ** (3 * exponent - t - 2)
        return (q - 1) ** 3 * total + q ** (2 * exponent - 2) * (exponent * (q - 1) + q) ** 2

    total = 0
    qm = q % modulus
    for t in range(1, exponent + 1):
        total = (total + (t * t % modulus) * pow(qm, 3 * exponent - t - 2, modulus)) % modulus

    term1 = pow((q - 1) % modulus, 3, modulus) * total % modulus
    term2 = pow(qm, 2 * exponent - 2, modulus) * ((exponent * (q - 1) + q) % modulus) ** 2 % modulus
    return (term1 + term2) % modulus


def gFromFactors(factors, modulus=None):
    result = 1
    for prime, exponent in factors.items():
        value = gPrimePower(prime, exponent, modulus)
        result = result * value if modulus is None else result * value % modulus
    return result


def fOfPrime(p, modulus=None):
    m = p - 1
    factors = factorize64(m)
    if modulus is None:
        return m * m + gFromFactors(factors)
    mm = m % modulus
    return (mm * mm + gFromFactors(factors, modulus)) % modulus


def primesInInterval(low, high, preSieveLimit=200_000):
    length = high - low + 1
    isComposite = bytearray(length)

    for prime in sievePrimes(preSieveLimit):
        start = (-low) % prime
        for index in range(start, length, prime):
            isComposite[index] = 1
        if low <= prime <= high:
            isComposite[prime - low] = 0

    for value in (0, 1):
        if low <= value <= high:
            isComposite[value - low] = 1

    for index, composite in enumerate(isComposite):
        if not composite:
            candidate = low + index
            if isPrime64(candidate):
                yield candidate


def S(low, high, modulus=MOD):
    total = 0
    for prime in primesInInterval(low, high):
        total = (total + fOfPrime(prime, modulus)) % modulus
    return total


def runTests():
    assert fOfPrime(5) == 104
    assert fOfPrime(97) == 1_614_336

    total100 = sum(fOfPrime(prime) for prime in sievePrimes(100))
    assert total100 == 7_381_000

    total100000 = 0
    for prime in sievePrimes(100_000):
        total100000 = (total100000 + fOfPrime(prime, MOD)) % MOD
    assert total100000 == 701_331_986


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(10 ** 16, 10 ** 16 + 10 ** 6, MOD)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
