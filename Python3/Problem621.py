from fractions import Fraction
from functools import lru_cache
import math
import time


TARGET = 17_526 * 10 ** 9


def factorInteger(n):
    factors = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2

    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            factors[factor] = factors.get(factor, 0) + 1
            n //= factor
        factor += 2

    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def divisorsFromFactors(factors):
    divisors = [1]
    for prime, exponent in factors.items():
        powers = [prime ** power for power in range(exponent + 1)]
        divisors = [divisor * power for divisor in divisors for power in powers]
    return divisors


def triangularNumbers(limit):
    numbers = []
    index = 0
    while True:
        value = index * (index + 1) // 2
        if value > limit:
            return numbers
        numbers.append(value)
        index += 1


def triangularTripleCountBrute(n):
    triangles = triangularNumbers(n)
    pairCounts = {}
    for first in triangles:
        for second in triangles:
            total = first + second
            if total <= n:
                pairCounts[total] = pairCounts.get(total, 0) + 1

    return sum(pairCounts.get(n - third, 0) for third in triangles)


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))
    if limit >= 1:
        factors[1] = 1

    for number in range(2, math.isqrt(limit) + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number

    return factors


def factorFromSmallestPrimeFactors(n, smallestFactors):
    factors = []
    while n > 1:
        prime = smallestFactors[n]
        exponent = 0
        while n % prime == 0:
            n //= prime
            exponent += 1
        factors.append((prime, exponent))
    return factors


def tonelliShanks(n, prime):
    n %= prime
    if n == 0:
        return 0
    if pow(n, (prime - 1) // 2, prime) != 1:
        return None
    if prime % 4 == 3:
        return pow(n, (prime + 1) // 4, prime)

    oddPart = prime - 1
    twoPower = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        twoPower += 1

    nonResidue = 2
    while pow(nonResidue, (prime - 1) // 2, prime) != prime - 1:
        nonResidue += 1

    modulusPower = twoPower
    c = pow(nonResidue, oddPart, prime)
    t = pow(n, oddPart, prime)
    root = pow(n, (oddPart + 1) // 2, prime)

    while t != 1:
        index = 1
        squared = (t * t) % prime
        while squared != 1:
            squared = (squared * squared) % prime
            index += 1

        b = pow(c, 1 << (modulusPower - index - 1), prime)
        modulusPower = index
        c = (b * b) % prime
        t = (t * c) % prime
        root = (root * b) % prime

    return root


def rootsPrimePower(discriminant, prime, exponent):
    modulus = prime ** exponent
    if discriminant % prime == 0:
        return [0] if exponent == 1 else []

    root = tonelliShanks(discriminant, prime)
    if root is None:
        return []

    roots = []
    for value in {root, (-root) % prime}:
        liftedRoot = value
        currentModulus = prime
        for _ in range(1, exponent):
            correction = ((discriminant - liftedRoot * liftedRoot) // currentModulus) % prime
            correction *= pow(2 * liftedRoot, -1, prime)
            correction %= prime
            liftedRoot += correction * currentModulus
            currentModulus *= prime
        roots.append(liftedRoot % modulus)

    return sorted(set(roots))


def rootsModOddA(discriminant, a, smallestFactors, cache):
    if a == 1:
        return [0]

    roots = [0]
    modulus = 1
    for prime, exponent in factorFromSmallestPrimeFactors(a, smallestFactors):
        key = (prime, exponent)
        if key not in cache:
            cache[key] = rootsPrimePower(discriminant, prime, exponent)
        primePowerRoots = cache[key]
        if not primePowerRoots:
            return []

        primePower = prime ** exponent
        inverse = pow(modulus, -1, primePower)
        combinedRoots = []
        for root in roots:
            for primePowerRoot in primePowerRoots:
                offset = ((primePowerRoot - root) % primePower) * inverse
                offset %= primePower
                combinedRoots.append((root + modulus * offset) % (modulus * primePower))

        roots = combinedRoots
        modulus *= primePower

    return roots


@lru_cache(maxsize=None)
def fundamentalClassNumber(discriminant):
    if discriminant in (-3, -4):
        return 1
    assert discriminant < 0
    assert discriminant % 8 == 5

    limit = math.isqrt((-discriminant) // 3)
    while 3 * (limit + 1) * (limit + 1) <= -discriminant:
        limit += 1

    smallestFactors = smallestPrimeFactors(limit)
    rootCache = {}
    count = 0
    for a in range(1, limit + 1, 2):
        for root in rootsModOddA(discriminant, a, smallestFactors, rootCache):
            oddRoot = root if root % 2 == 1 else root + a
            b = oddRoot if oddRoot <= a else oddRoot - 2 * a
            c = (b * b - discriminant) // (4 * a)

            if a <= c and (a < c or b >= 0):
                count += 1

    return count


def kroneckerForOddPrime(discriminant, prime):
    if discriminant % prime == 0:
        return 0
    return 1 if pow(discriminant % prime, (prime - 1) // 2, prime) == 1 else -1


def ringClassNumber(fundamentalDiscriminant, conductor):
    baseClassNumber = fundamentalClassNumber(fundamentalDiscriminant)
    value = Fraction(baseClassNumber * conductor, 1)
    for prime in factorInteger(conductor):
        symbol = kroneckerForOddPrime(fundamentalDiscriminant, prime)
        value *= Fraction(prime - symbol, prime)

    if conductor > 1 and fundamentalDiscriminant == -3:
        value /= 3
    elif conductor > 1 and fundamentalDiscriminant == -4:
        value /= 2

    assert value.denominator == 1
    return value.numerator


def hurwitzClassNumberForThreeSquares(n):
    factors = factorInteger(n)
    squareFreePart = 1
    conductorFactors = {}
    for prime, exponent in factors.items():
        if exponent % 2 == 1:
            squareFreePart *= prime
        if exponent // 2:
            conductorFactors[prime] = exponent // 2

    fundamentalDiscriminant = -squareFreePart
    total = Fraction(0, 1)
    for conductor in divisorsFromFactors(conductorFactors):
        if conductor == 1 and fundamentalDiscriminant == -3:
            total += Fraction(1, 3)
        elif conductor == 1 and fundamentalDiscriminant == -4:
            total += Fraction(1, 2)
        else:
            total += ringClassNumber(fundamentalDiscriminant, conductor)

    return total


def triangularTripleCount(n):
    # 8*T_k+1=(2k+1)^2, so G(n)=r_3(8n+3)/8=3*H(8n+3).
    total = 3 * hurwitzClassNumberForThreeSquares(8 * n + 3)
    assert total.denominator == 1
    return total.numerator


def runTests():
    assert triangularTripleCountBrute(9) == 7
    assert triangularTripleCountBrute(1_000) == 78

    assert triangularTripleCount(9) == 7
    assert triangularTripleCount(1_000) == 78
    assert triangularTripleCount(10 ** 6) == 2_106


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triangularTripleCount(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
