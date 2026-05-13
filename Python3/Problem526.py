import heapq
import math
import time
from dataclasses import dataclass
from fractions import Fraction


BASE_MODULUS = 2 ** 3 * 3 ** 2 * 5 * 7
BASE_PRIME_POWERS = ((2, 3), (3, 2), (5, 1), (7, 1))
WHEEL_PRIMES = (11, 13, 17, 19, 23, 29)
MILLER_RABIN_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


@dataclass(frozen=True)
class ResidueInfo:
    residue: int
    topStart: int
    cofactors: tuple[int, ...]
    coefficient: Fraction
    upperBound: int


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )
    return [number for number in range(limit + 1) if sieve[number]]


PRIMALITY_TRIAL_PRIMES = tuple(primeSieve(200))
PRIME_TUPLE_EXTRA_TRIAL_PRIMES = tuple(
    prime for prime in PRIMALITY_TRIAL_PRIMES if prime > max(WHEEL_PRIMES)
)
SMALL_PRIMES = tuple(primeSieve(100_000))


def isPrime(n):
    if n < 2:
        return False

    for prime in PRIMALITY_TRIAL_PRIMES:
        if n % prime == 0:
            return n == prime

    oddPart = n - 1
    powersOfTwo = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        powersOfTwo += 1

    for base in MILLER_RABIN_BASES:
        if base % n == 0:
            continue
        value = pow(base, oddPart, n)
        if value == 1 or value == n - 1:
            continue
        for _ in range(powersOfTwo - 1):
            value = value * value % n
            if value == n - 1:
                break
        else:
            return False

    return True


def pollardRho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    constant = 1
    while True:
        x = 2
        y = 2
        divisor = 1
        while divisor == 1:
            x = (x * x + constant) % n
            y = (y * y + constant) % n
            y = (y * y + constant) % n
            divisor = math.gcd(abs(x - y), n)
        if divisor != n:
            return divisor
        constant += 1


def factorize(n, factors):
    if n == 1:
        return
    if isPrime(n):
        factors.append(n)
        return

    divisor = pollardRho(n)
    factorize(divisor, factors)
    factorize(n // divisor, factors)


def largestPrimeFactor(n):
    remaining = n
    largest = 1

    for prime in SMALL_PRIMES:
        if prime * prime > remaining:
            break
        while remaining % prime == 0:
            largest = prime
            remaining //= prime

    if remaining == 1:
        return largest
    if isPrime(remaining):
        return max(largest, remaining)

    factors = []
    factorize(remaining, factors)
    return max(largest, max(factors))


def consecutiveLargestPrimeFactorSum(start):
    return sum(largestPrimeFactor(start + offset) for offset in range(9))


def forcedCofactors(residue):
    cofactors = []
    for offset in range(9):
        value = residue + offset
        cofactor = 1
        for prime, exponent in BASE_PRIME_POWERS:
            primePower = 1
            for _ in range(exponent):
                if value % (primePower * prime) == 0:
                    primePower *= prime
                else:
                    break
            cofactor *= primePower
        cofactors.append(cofactor)
    return tuple(cofactors)


def upperBound(start, cofactors):
    return sum((start + offset) // cofactors[offset] for offset in range(9))


def residueInfos(limit):
    infos = []
    for residue in range(BASE_MODULUS):
        topStart = limit - ((limit - residue) % BASE_MODULUS)
        if topStart < 2:
            continue

        cofactors = forcedCofactors(residue)
        coefficient = sum(Fraction(1, cofactor) for cofactor in cofactors)
        infos.append(
            ResidueInfo(
                residue,
                topStart,
                cofactors,
                coefficient,
                upperBound(topStart, cofactors),
            )
        )

    return sorted(infos, key=lambda info: info.upperBound, reverse=True)


def bruteForceMaximum(limit):
    best = 0
    for start in range(2, limit + 1):
        best = max(best, consecutiveLargestPrimeFactorSum(start))
    return best


def exactBoundedSearch(limit):
    best = 0
    for info in residueInfos(limit):
        if info.upperBound <= best:
            break

        start = info.topStart
        while start >= 2 and upperBound(start, info.cofactors) > best:
            best = max(best, consecutiveLargestPrimeFactorSum(start))
            start -= BASE_MODULUS

    return best


def allowedWheelResidues(topStart):
    residues = [0]
    modulus = 1

    for prime in WHEEL_PRIMES:
        inverseBase = pow(BASE_MODULUS, -1, prime)
        forbidden = {
            ((topStart + offset) % prime) * inverseBase % prime
            for offset in range(9)
        }

        nextResidues = []
        for residue in residues:
            for step in range(prime):
                candidate = residue + modulus * step
                if candidate % prime not in forbidden:
                    nextResidues.append(candidate)

        residues = nextResidues
        modulus *= prime

    residues.sort()
    return residues, modulus


def primeTupleCandidates(info):
    residues, wheelModulus = allowedWheelResidues(info.topStart)
    maxStep = (info.topStart - 2) // BASE_MODULUS

    cycle = 0
    while cycle * wheelModulus <= maxStep:
        baseStep = cycle * wheelModulus
        for residue in residues:
            step = baseStep + residue
            if step > maxStep:
                break
            yield info.topStart - BASE_MODULUS * step
        cycle += 1


def hasPrimeQuotients(start, cofactors):
    for prime in PRIME_TUPLE_EXTRA_TRIAL_PRIMES:
        residue = start % prime
        for offset in range(9):
            if (residue + offset) % prime == 0:
                return False

    for offset, cofactor in enumerate(cofactors):
        value = start + offset
        if value % cofactor != 0:
            return False
        if not isPrime(value // cofactor):
            return False
    return True


def findBestPrimeTuple(limit, topInfos):
    streams = [primeTupleCandidates(info) for info in topInfos]
    heap = []

    for index, stream in enumerate(streams):
        start = next(stream, None)
        if start is not None:
            info = topInfos[index]
            heapq.heappush(heap, (-upperBound(start, info.cofactors), index, start))

    while heap:
        negativeBound, index, start = heapq.heappop(heap)
        info = topInfos[index]
        candidateBound = -negativeBound

        if hasPrimeQuotients(start, info.cofactors):
            return candidateBound, start, info

        nextStart = next(streams[index], None)
        if nextStart is not None:
            heapq.heappush(
                heap, (-upperBound(nextStart, info.cofactors), index, nextStart)
            )

    raise RuntimeError("No prime quotient tuple found")


def verifyLargeSearchCertificate(best, infos):
    challengers = [info for info in infos if info.upperBound > best]
    if not challengers:
        return

    maxCoefficient = max(info.coefficient for info in infos)
    for info in challengers:
        if info.coefficient != maxCoefficient:
            raise RuntimeError("Unexpected lower-coefficient challenger")

        smallestQuotient = min(
            (info.topStart + offset) // info.cofactors[offset]
            for offset in range(9)
        )
        if info.upperBound - best >= smallestQuotient // 2:
            raise RuntimeError("Composite quotient bound is too weak")


def largeMaximumConsecutiveSum(limit):
    infos = residueInfos(limit)
    maxCoefficient = max(info.coefficient for info in infos)
    topInfos = [info for info in infos if info.coefficient == maxCoefficient]

    best, _, _ = findBestPrimeTuple(limit, topInfos)
    verifyLargeSearchCertificate(best, infos)
    return best


def maximumConsecutiveSum(limit):
    if limit <= 10_000:
        return bruteForceMaximum(limit)
    if limit <= 10 ** 9:
        return exactBoundedSearch(limit)
    if limit == 10 ** 16:
        return largeMaximumConsecutiveSum(limit)

    raise ValueError("large search certificate is implemented for the problem target")


def runTests():
    assert largestPrimeFactor(100) == 5
    assert largestPrimeFactor(101) == 101
    assert consecutiveLargestPrimeFactorSum(100) == 409
    assert maximumConsecutiveSum(100) == 417
    assert maximumConsecutiveSum(10 ** 9) == 4_896_292_593


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumConsecutiveSum(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
