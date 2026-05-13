from array import array
import time


def mobius(limit):
    leastPrime = array("I", [0]) * (limit + 1)
    mu = array("b", [0]) * (limit + 1)
    mu[1] = 1
    primes = []

    for n in range(2, limit + 1):
        if leastPrime[n] == 0:
            leastPrime[n] = n
            primes.append(n)
            mu[n] = -1

        least = leastPrime[n]
        muN = mu[n]
        for prime in primes:
            value = n * prime
            if value > limit or prime > least:
                break
            leastPrime[value] = prime
            if prime == least:
                mu[value] = 0
                break
            mu[value] = -muN

    return mu


def _count_small(limit):
    mu = mobius(limit)
    plus = [0] * (limit + 1)
    minus = [0] * (limit + 1)
    for n in range(1, limit + 1):
        plus[n] = plus[n - 1] + (1 if mu[n] == 1 else 0)
        minus[n] = minus[n - 1] + (1 if mu[n] == -1 else 0)

    total = 0
    for a in range(1, limit + 1):
        before = a - 1
        for b in range(a, limit + 1):
            p = plus[b] - plus[before]
            n = minus[b] - minus[before]
            if 99 * n <= 100 * p and 99 * p <= 100 * n:
                total += 1
    return total


def countPositiveIntervals(mu, plusWeight, minusWeight):
    current = 0
    minimum = 0
    maximum = 0
    for n in range(1, len(mu)):
        if mu[n] == 1:
            current += plusWeight
        elif mu[n] == -1:
            current += minusWeight
        if current < minimum:
            minimum = current
        elif current > maximum:
            maximum = current

    span = maximum - minimum + 1
    tree = array("i", [0]) * (span + 2)

    def add(index):
        while index <= span + 1:
            tree[index] += 1
            index += index & -index

    def prefixSum(index):
        total = 0
        while index > 0:
            total += tree[index]
            index -= index & -index
        return total

    current = 0
    positives = 0
    add(-minimum + 1)
    for n in range(1, len(mu)):
        if mu[n] == 1:
            current += plusWeight
        elif mu[n] == -1:
            current += minusWeight
        index = current - minimum + 1
        positives += prefixSum(index - 1)
        add(index)

    return positives


def intervalCount(limit):
    mu = mobius(limit)
    intervals = limit * (limit + 1) // 2
    tooManyPositive = countPositiveIntervals(mu, 99, -100)
    tooManyNegative = countPositiveIntervals(mu, -100, 99)
    return intervals - tooManyPositive - tooManyNegative


def runTests():
    assert mobius(10)[1:].tolist() == [1, -1, -1, 0, -1, 1, -1, 0, 0, 1]
    assert intervalCount(10) == 13
    assert intervalCount(500) == 16676


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = intervalCount(20_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
