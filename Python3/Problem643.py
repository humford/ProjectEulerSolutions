from array import array
import math
import time


MODULUS = 1_000_000_007
INVERSE_TWO = (MODULUS + 1) // 2
PREFIX_LIMIT = 2_000_000


totientPrefix = None
totientPrefixCache = {}


def isTwoFriendly(first, second):
    gcd = math.gcd(first, second)
    return gcd > 1 and gcd & (gcd - 1) == 0


def twoFriendlyPairCountBrute(limit):
    return sum(
        1
        for first in range(1, limit + 1)
        for second in range(first + 1, limit + 1)
        if isTwoFriendly(first, second)
    )


def buildTotientPrefix(limit):
    totients = array("Q", range(limit + 1))
    for number in range(2, limit + 1):
        if totients[number] == number:
            for multiple in range(number, limit + 1, number):
                totients[multiple] -= totients[multiple] // number

    prefix = array("I", [0]) * (limit + 1)
    total = 0
    for number in range(1, limit + 1):
        total = (total + totients[number]) % MODULUS
        prefix[number] = total
    return prefix


def ensureTotientPrefix():
    global totientPrefix
    if totientPrefix is None:
        totientPrefix = buildTotientPrefix(PREFIX_LIMIT)
    return totientPrefix


def totientSummatory(limit):
    if limit <= PREFIX_LIMIT:
        return ensureTotientPrefix()[limit]
    if limit in totientPrefixCache:
        return totientPrefixCache[limit]

    total = (limit % MODULUS) * ((limit + 1) % MODULUS) * INVERSE_TWO % MODULUS
    start = 2
    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        total -= ((end - start + 1) % MODULUS) * totientSummatory(quotient)
        total %= MODULUS
        start = end + 1

    totientPrefixCache[limit] = total
    return total


def twoFriendlyPairCount(limit):
    total = 0
    powerOfTwo = 2
    while powerOfTwo <= limit:
        # Divide both numbers by the exact common factor 2^t; the remaining
        # unordered pair must be coprime, counted by sum_{m=2..n} phi(m).
        total += totientSummatory(limit // powerOfTwo) - 1
        total %= MODULUS
        powerOfTwo *= 2
    return total


def runTests():
    assert isTwoFriendly(24, 40)
    assert not isTwoFriendly(24, 36)
    assert twoFriendlyPairCountBrute(100) == 1_031
    assert twoFriendlyPairCount(100) == 1_031
    assert twoFriendlyPairCount(10 ** 6) == 321_418_433


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = twoFriendlyPairCount(10 ** 11)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
