from array import array
from math import isqrt
import time


def euclidSteps(x, y):
    steps = 0
    while y:
        x, y = y, x % y
        steps += 1
    return steps


def bruteS(limit):
    return sum(
        euclidSteps(x, y)
        for x in range(1, limit + 1)
        for y in range(1, limit + 1)
    )


def floorSumPair(p, q, m, s1, s2):
    sum1 = 0
    sum2 = 0
    sign = 1

    while True:
        quotient = m // q
        m -= quotient * q
        sum1 += sign * quotient * s1
        sum2 += sign * quotient * s2

        quotient = p // q
        p -= quotient * q
        sum1 += sign * quotient * s1 * (s1 + 1) // 2
        sum2 += sign * quotient * s2 * (s2 + 1) // 2

        if p == 0:
            return sum1, sum2

        quotient = (p * s1 + m) // q
        sum1 += sign * s1 * quotient
        s1 = quotient

        quotient = (p * s2 + m) // q
        sum2 += sign * s2 * quotient
        s2 = quotient

        p, q = q, p
        m = -m - 1
        sign = -sign


def coprimeEuclidTreeSum(limit):
    root = isqrt(limit)
    first = 0
    second = 0

    for x in range(2, root + 1):
        for y in range(1, x):
            split = limit // (x + y)
            first += split * (split - 1) // 2

            s1 = limit // x - split
            s2 = root - split if split <= root else 0
            block1, block2 = floorSumPair(-x, y, limit - split * x, s1, s2)
            first += block1

            if split <= root:
                second += split * (split - 1) // 2 + block2
            else:
                second += root * (root - 1) // 2

    return 2 * first - second


def mobiusPrefix(limit):
    leastPrime = array("I", [0]) * (limit + 1)
    mu = array("b", [0]) * (limit + 1)
    prefix = array("i", [0]) * (limit + 1)
    primes = []
    if limit >= 1:
        mu[1] = 1

    for n in range(2, limit + 1):
        if leastPrime[n] == 0:
            leastPrime[n] = n
            primes.append(n)
            mu[n] = -1
        least = leastPrime[n]
        muN = mu[n]
        for prime in primes:
            value = n * prime
            if value > limit:
                break
            leastPrime[value] = prime
            if prime == least:
                mu[value] = 0
                break
            mu[value] = -muN

    total = 0
    for n in range(1, limit + 1):
        total += mu[n]
        prefix[n] = total
    return prefix


def baseTerm(limit):
    half = limit // 2
    if limit % 2 == 0:
        return (3 * half - 2) * half
    return 3 * half * half + half


def euclidStepSum(limit):
    if limit < 5:
        return bruteS(limit)

    mobius = mobiusPrefix(limit // 5)
    subtotal = baseTerm(limit)
    start = 1
    while start <= limit // 5:
        quotient = limit // start
        end = min(limit // 5, limit // quotient)
        muSum = mobius[end] - mobius[start - 1]
        if muSum and quotient > 1:
            subtotal += 2 * muSum * coprimeEuclidTreeSum(quotient)
        start = end + 1

    return 2 * subtotal + limit * (limit + 1) // 2


def runTests():
    assert euclidSteps(1, 1) == 1
    assert euclidSteps(10, 6) == 3
    assert euclidSteps(6, 10) == 4
    assert bruteS(1) == 1
    assert bruteS(10) == 221
    assert bruteS(100) == 39826
    assert euclidStepSum(10) == 221
    assert euclidStepSum(100) == 39826
    assert euclidStepSum(1000) == 5_893_024


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = euclidStepSum(5_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
