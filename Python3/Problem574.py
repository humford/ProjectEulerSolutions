import math
import time


def primeSieve(limit):
    isPrime = [True] * (limit + 1)
    isPrime[0] = False
    isPrime[1] = False

    for number in range(2, math.isqrt(limit) + 1):
        if isPrime[number]:
            for multiple in range(number * number, limit + 1, number):
                isPrime[multiple] = False

    return [number for number in range(limit + 1) if isPrime[number]]


def primorialSplits(primes, q):
    smallPrimes = [prime for prime in primes if prime < q]
    product = math.prod(smallPrimes)
    splits = []

    for mask in range(1 << len(smallPrimes)):
        left = 1
        for index, prime in enumerate(smallPrimes):
            if mask & (1 << index):
                left *= prime
        splits.append((left, product // left))

    return product, splits


def firstCandidateInRange(residue, modulus, lower, upper):
    candidate = residue

    if candidate < lower:
        candidate += ((lower - candidate + modulus - 1) // modulus) * modulus

    if candidate <= upper:
        return candidate
    return None


def verifierValueWithPrimes(p, primes, splitCache):
    q = next(prime for prime in primes if prime * prime > p)
    modulus, splits = splitCache[q]
    best = None

    for left, right in splits:
        if right == 1:
            residue = 0
        else:
            residue = (left * ((p * pow(left % right, -1, right)) % right)) % modulus

        candidate = firstCandidateInRange(residue, modulus, (p + 1) // 2, p - 1)
        if candidate is not None and math.gcd(candidate, p - candidate) == 1:
            if best is None or candidate < best:
                best = candidate

        candidate = firstCandidateInRange(residue, modulus, p + 1, 10 ** 30)
        if candidate is not None and math.gcd(candidate, candidate - p) == 1:
            if best is None or candidate < best:
                best = candidate

    return best


def verifierValue(p):
    primes = primeSieve(max(10, p + 10))
    q = next(prime for prime in primes if prime * prime > p)
    splitCache = {q: primorialSplits(primes, q)}
    return verifierValueWithPrimes(p, primes, splitCache)


def verifierSum(limit):
    primes = primeSieve(limit)
    largestNeededQ = next(prime for prime in primes if prime * prime > limit - 1)
    splitCache = {
        prime: primorialSplits(primes, prime)
        for prime in primes
        if prime <= largestNeededQ
    }

    total = 0
    for prime in primes:
        if prime >= limit:
            break
        total += verifierValueWithPrimes(prime, primes, splitCache)

    return total


def runTests():
    assert verifierValue(2) == 1
    assert verifierValue(37) == 22
    assert verifierValue(151) == 165
    assert verifierSum(10) == 10
    assert verifierSum(200) == 7_177


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = verifierSum(3_800)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
