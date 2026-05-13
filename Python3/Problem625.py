from array import array
import math
import time


MODULUS = 998_244_353
INVERSE_TWO = (MODULUS + 1) // 2
PREFIX_LIMIT = 4_000_000


totientPrefix = None
totientPrefixCache = {}


def gcdSumBrute(limit):
    return sum(math.gcd(i, j) for j in range(1, limit + 1) for i in range(1, j + 1))


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

    total = (limit % MODULUS) * ((limit + 1) % MODULUS) * INVERSE_TWO
    total %= MODULUS

    start = 2
    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        total -= ((end - start + 1) % MODULUS) * totientSummatory(quotient)
        total %= MODULUS
        start = end + 1

    totientPrefixCache[limit] = total
    return total


def triangular(value):
    value %= MODULUS
    return value * ((value + 1) % MODULUS) * INVERSE_TWO % MODULUS


def gcdSum(limit):
    total = 0
    start = 1
    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        totientBlock = (totientSummatory(end) - totientSummatory(start - 1)) % MODULUS
        total += totientBlock * triangular(quotient)
        total %= MODULUS
        start = end + 1

    return total


def runTests():
    assert gcdSumBrute(10) == 122
    assert gcdSum(10) == 122
    assert gcdSum(50) == gcdSumBrute(50) % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gcdSum(10 ** 11)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
