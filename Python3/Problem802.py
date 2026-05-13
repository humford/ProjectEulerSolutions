import time
from array import array


MOD = 1_020_340_567


def floorDivisionQueries(n):
    queries = set()
    k = 1
    while k <= n:
        quotient = n // k
        queries.add(quotient)
        k = n // quotient + 1
    return sorted(queries)


def mertensAtPoints(limit, points):
    points = sorted(set(points))
    result = {}
    if not points:
        return result

    mobius = array("b", [0]) * (limit + 1)
    leastPrime = array("I", [0]) * (limit + 1)
    primes = []
    mobius[1] = 1
    mertens = 1

    index = 0
    if points[index] == 1:
        result[1] = 1
        index += 1

    for n in range(2, limit + 1):
        if leastPrime[n] == 0:
            leastPrime[n] = n
            primes.append(n)
            mobius[n] = -1

        limitPrime = leastPrime[n]
        muN = mobius[n]
        for prime in primes:
            if prime > limitPrime:
                break
            value = n * prime
            if value > limit:
                break
            leastPrime[value] = prime
            if prime == limitPrime:
                mobius[value] = 0
                break
            mobius[value] = -muN

        mertens += mobius[n]
        if index < len(points) and n == points[index]:
            result[n] = mertens
            index += 1

    return result


def P(n, modulus=MOD):
    if n <= 0:
        return 0

    queries = floorDivisionQueries(n)
    mertens = mertensAtPoints(n, queries)
    powerCache = {0: 1}

    def pow2(exponent):
        value = powerCache.get(exponent)
        if value is None:
            value = pow(2, exponent, modulus)
            powerCache[exponent] = value
        return value

    def sumA(left, right):
        if left == 1:
            return pow2(right)
        return (pow2(right) - pow2(left - 1)) % modulus

    total = 0
    left = 1
    while left <= n:
        quotient = n // left
        right = n // quotient
        total = (total + sumA(left, right) * mertens[quotient]) % modulus
        left = right + 1

    return total


def runTests():
    assert P(1) == 2
    assert P(2) == 2
    assert P(3) == 4


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = P(10_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
