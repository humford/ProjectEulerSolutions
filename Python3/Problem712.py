import math
import time


MODULUS = 1_000_000_007
SMALL_PRIME_LIMIT = 100_000_000


def simplePrimesAndPi(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        isPrime[0] = 0
    if limit >= 1:
        isPrime[1] = 0

    for n in range(2, math.isqrt(limit) + 1):
        if isPrime[n]:
            start = n * n
            isPrime[start : limit + 1 : n] = b"\x00" * (((limit - start) // n) + 1)

    primes = []
    primePi = [0] * (limit + 1)
    count = 0
    for n in range(limit + 1):
        if isPrime[n]:
            primes.append(n)
            count += 1
        primePi[n] = count

    return primes, primePi


def segmentedPrimesUpTo(limit, segmentSize=1 << 20):
    if limit < 2:
        return

    yield 2
    basePrimes, _ = simplePrimesAndPi(math.isqrt(limit))
    basePrimes = [prime for prime in basePrimes if prime != 2]

    low = 3
    step = 2 * segmentSize
    while low <= limit:
        high = min(low + step - 2, limit)
        size = (high - low) // 2 + 1
        sieve = bytearray(size)

        for prime in basePrimes:
            primeSquared = prime * prime
            if primeSquared > high:
                break

            start = primeSquared if primeSquared >= low else ((low + prime - 1) // prime) * prime
            if start % 2 == 0:
                start += prime

            index = (start - low) // 2
            if index < size:
                sieve[index::prime] = b"\x01" * (((size - index - 1) // prime) + 1)

        for i, isComposite in enumerate(sieve):
            if isComposite == 0:
                yield low + 2 * i

        low += step


class PrimeCounter:
    def __init__(self, limit):
        self.limit = limit
        self.primes, self.primePi = simplePrimesAndPi(limit)
        self.phiCache = {}
        self.piCache = {}

    def phi(self, x, a):
        if a == 0:
            return x
        if a == 1:
            return x - x // 2

        key = (x, a)
        if key not in self.phiCache:
            self.phiCache[key] = self.phi(x, a - 1) - self.phi(x // self.primes[a - 1], a - 1)
        return self.phiCache[key]

    def pi(self, x):
        if x <= self.limit:
            return self.primePi[x]
        if x in self.piCache:
            return self.piCache[x]

        fourth = int(x ** 0.25)
        while (fourth + 1) ** 4 <= x:
            fourth += 1
        while fourth ** 4 > x:
            fourth -= 1

        square = math.isqrt(x)
        cube = int(round(x ** (1 / 3)))
        while (cube + 1) ** 3 <= x:
            cube += 1
        while cube ** 3 > x:
            cube -= 1

        a = self.pi(fourth)
        b = self.pi(square)
        c = self.pi(cube)

        result = self.phi(x, a) + (b + a - 2) * (b - a + 1) // 2

        for i in range(a + 1, b + 1):
            w = x // self.primes[i - 1]
            result -= self.pi(w)
            if i <= c:
                limit = self.pi(math.isqrt(w))
                for j in range(i, limit + 1):
                    result -= self.pi(w // self.primes[j - 1]) - j + 1

        self.piCache[x] = result
        return result


def primeExponentMap(number):
    exponents = {}
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            exponents[divisor] = exponents.get(divisor, 0) + 1
            number //= divisor
        divisor += 1 if divisor == 2 else 2

    if number > 1:
        exponents[number] = exponents.get(number, 0) + 1

    return exponents


def exponentDifference(first, second):
    left = primeExponentMap(first)
    right = primeExponentMap(second)
    return sum(abs(left.get(prime, 0) - right.get(prime, 0)) for prime in set(left) | set(right))


def contribution(quotient, limit):
    return quotient * (limit - quotient)


def exponentDifferenceSum(limit):
    cutoff = min(SMALL_PRIME_LIMIT, limit)
    total = 0

    for prime in segmentedPrimesUpTo(cutoff):
        power = prime
        while power <= limit:
            quotient = limit // power
            total = (total + contribution(quotient, limit)) % MODULUS
            if power > limit // prime:
                break
            power *= prime

    if cutoff < limit:
        counter = PrimeCounter(math.isqrt(limit))
        maxQuotient = limit // (cutoff + 1)
        for quotient in range(1, maxQuotient + 1):
            high = limit // quotient
            low = max(cutoff, limit // (quotient + 1))
            count = counter.pi(high) - counter.pi(low)
            if count:
                total = (total + (count % MODULUS) * contribution(quotient, limit)) % MODULUS

    return (2 * total) % MODULUS


def runTests():
    assert exponentDifference(14, 24) == 4
    assert exponentDifferenceSum(10) == 210
    assert exponentDifferenceSum(10 ** 2) == 37_018


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = exponentDifferenceSum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
