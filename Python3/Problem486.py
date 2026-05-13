import itertools
import math
import time


MODULUS = 87_654_321
PALINDROME_FREE_PERIOD_START = 7
PALINDROME_FREE_PERIOD = 6


def _has_long_palindrome(bits):
    for length in range(5, len(bits) + 1):
        for start in range(len(bits) - length + 1):
            piece = bits[start:start + length]
            if piece == piece[::-1]:
                return True
    return False


def palindromeFreeExactCounts(limit):
    states = {"": 1}
    counts = [1]

    for _ in range(limit):
        nextStates = {}
        for suffix, count in states.items():
            for bit in "01":
                candidate = suffix + bit
                if len(candidate) >= 5 and candidate[-5:] == candidate[-5:][::-1]:
                    continue
                if len(candidate) >= 6 and candidate[-6:] == candidate[-6:][::-1]:
                    continue

                nextSuffix = candidate[-5:]
                nextStates[nextSuffix] = nextStates.get(nextSuffix, 0) + count

        states = nextStates
        counts.append(sum(states.values()))

    return counts


PALINDROME_FREE_EXACT = palindromeFreeExactCounts(18)
PALINDROME_FREE_CUMULATIVE_SMALL = [
    sum(PALINDROME_FREE_EXACT[:index + 1]) for index in range(PALINDROME_FREE_PERIOD_START)
]
PALINDROME_FREE_PERIOD_VALUES = tuple(
    PALINDROME_FREE_EXACT[
        PALINDROME_FREE_PERIOD_START:
        PALINDROME_FREE_PERIOD_START + PALINDROME_FREE_PERIOD
    ]
)
PALINDROME_FREE_PERIOD_PREFIX = [0]
for value in PALINDROME_FREE_PERIOD_VALUES:
    PALINDROME_FREE_PERIOD_PREFIX.append(PALINDROME_FREE_PERIOD_PREFIX[-1] + value)


def palindromeStringCount(limit):
    total = 0
    for length in range(1, limit + 1):
        for bits in itertools.product("01", repeat=length):
            if _has_long_palindrome("".join(bits)):
                total += 1
    return total


def palindromeFreeCumulativeCount(limit):
    if limit < PALINDROME_FREE_PERIOD_START:
        return PALINDROME_FREE_CUMULATIVE_SMALL[limit]

    fullPeriods, remainder = divmod(
        limit - (PALINDROME_FREE_PERIOD_START - 1),
        PALINDROME_FREE_PERIOD,
    )
    return (
        PALINDROME_FREE_CUMULATIVE_SMALL[PALINDROME_FREE_PERIOD_START - 1]
        + fullPeriods * PALINDROME_FREE_PERIOD_PREFIX[-1]
        + PALINDROME_FREE_PERIOD_PREFIX[remainder]
    )


def fastPalindromeStringCount(limit):
    return (1 << (limit + 1)) - 1 - palindromeFreeCumulativeCount(limit)


def primeFactorization(n):
    factors = {}
    factor = 2
    while factor * factor <= n:
        while n % factor == 0:
            factors[factor] = factors.get(factor, 0) + 1
            n //= factor
        factor += 1 if factor == 2 else 2

    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def eulerPhi(n):
    result = n
    for prime in primeFactorization(n):
        result = result // prime * (prime - 1)
    return result


def multiplicativeOrder(base, modulus):
    if math.gcd(base, modulus) != 1:
        raise ValueError("base and modulus must be coprime")

    order = eulerPhi(modulus)
    for prime in primeFactorization(order):
        while order % prime == 0 and pow(base, order // prime, modulus) == 1:
            order //= prime
    return order


def _residueLimits(limit, order, combinedPeriod):
    base = 0
    remainders = [0] * PALINDROME_FREE_PERIOD

    for residue in range(PALINDROME_FREE_PERIOD):
        maxQuotient = (limit - residue - 6) // PALINDROME_FREE_PERIOD
        if maxQuotient < 0:
            continue

        count = maxQuotient + 1
        fullPeriods, remainder = divmod(count, combinedPeriod)
        base += fullPeriods * order
        remainders[residue] = remainder

    return base, remainders


def divisibleCounts(*limits):
    order = multiplicativeOrder(64, MODULUS)
    combinedPeriod = MODULUS * order
    inverse200 = pow(200, -1, MODULUS)
    inverseOrder = pow(order, -1, MODULUS)
    periodTotal = PALINDROME_FREE_PERIOD_PREFIX[-1]
    cumulativeBeforePeriod = PALINDROME_FREE_CUMULATIVE_SMALL[
        PALINDROME_FREE_PERIOD_START - 1
    ]

    preparedLimits = [
        _residueLimits(limit, order, combinedPeriod) for limit in limits
    ]
    extras = [0] * len(limits)

    powersOfTwo = [
        pow(2, residue + 7, MODULUS)
        for residue in range(PALINDROME_FREE_PERIOD)
    ]
    constants = [
        (1 + cumulativeBeforePeriod + PALINDROME_FREE_PERIOD_PREFIX[residue])
        % MODULUS
        for residue in range(PALINDROME_FREE_PERIOD)
    ]

    power64 = 1
    for quotientResidue in range(order):
        for residue in range(PALINDROME_FREE_PERIOD):
            left = powersOfTwo[residue] * power64 % MODULUS
            quotientModModulus = (
                (left - constants[residue]) * inverse200
            ) % MODULUS

            difference = quotientModModulus - quotientResidue
            if difference < 0:
                difference += MODULUS

            multiplier = difference * inverseOrder % MODULUS
            combinedResidue = quotientResidue + order * multiplier

            for index, (_, remainders) in enumerate(preparedLimits):
                if combinedResidue < remainders[residue]:
                    extras[index] += 1

        power64 = power64 * 64 % MODULUS

    return tuple(base + extra for (base, _), extra in zip(preparedLimits, extras))


def divisibleCount(limit):
    return divisibleCounts(limit)[0]


def runTests():
    assert PALINDROME_FREE_PERIOD_VALUES == (32, 32, 32, 34, 36, 34)
    assert PALINDROME_FREE_EXACT[13:19] == list(PALINDROME_FREE_PERIOD_VALUES)
    assert palindromeStringCount(4) == 0
    assert palindromeStringCount(5) == 8
    assert palindromeStringCount(6) == 42
    assert palindromeStringCount(11) == 3_844
    assert fastPalindromeStringCount(11) == palindromeStringCount(11)

    count10m, count5b = divisibleCounts(10 ** 7, 5 * 10 ** 9)
    assert count10m == 0
    assert count5b == 51


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisibleCount(10 ** 18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
