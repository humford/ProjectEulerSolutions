import time


def smallestPrimeFactorSieve(limit):
    smallestPrimeFactor = [0] * (limit + 1)
    smallestPrimeFactor[1] = 1
    primes = []

    for n in range(2, limit + 1):
        if smallestPrimeFactor[n] == 0:
            smallestPrimeFactor[n] = n
            primes.append(n)

        for prime in primes:
            value = n * prime
            if value > limit or prime > smallestPrimeFactor[n]:
                break
            smallestPrimeFactor[value] = prime

    return smallestPrimeFactor


def appendFactorsUpTo(factors, value, limit, smallestPrimeFactor):
    while value > 1:
        prime = smallestPrimeFactor[value]
        if prime > limit:
            break

        exponent = 1
        value //= prime
        while value > 1 and smallestPrimeFactor[value] == prime:
            exponent += 1
            value //= prime

        factors.append((prime, exponent))


def divisorsUpTo(factors, limit):
    divisors = [1]

    for prime, exponent in factors:
        newDivisors = []
        primePower = 1

        for _ in range(exponent + 1):
            for divisor in divisors:
                value = divisor * primePower
                if value <= limit:
                    newDivisors.append(value)
            primePower *= prime
            if primePower > limit:
                break

        divisors = newDivisors

    return divisors


def F(N):
    if N <= 2:
        return 0

    smallestPrimeFactor = smallestPrimeFactorSieve(N + 1)
    total = 0

    for r in range(2, N):
        maxK = min(r - 1, N - r)
        if maxK == 1:
            nValue = r * r - 1
            total += 2 * r + 1 + nValue
            continue

        left = r - 1
        right = r + 1
        factors = []

        if r % 2:
            leftTwos = (left & -left).bit_length() - 1
            rightTwos = (right & -right).bit_length() - 1
            left >>= leftTwos
            right >>= rightTwos
            if maxK >= 2:
                factors.append((2, leftTwos + rightTwos))

        appendFactorsUpTo(factors, left, maxK, smallestPrimeFactor)
        appendFactorsUpTo(factors, right, maxK, smallestPrimeFactor)

        nValue = r * r - 1
        base = 2 * r
        for k in divisorsUpTo(factors, maxK):
            total += base + k + nValue // k

    return total


def runTests():
    assert F(5) == 59
    assert F(10 ** 2) == 697_317


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = F(2 * 10 ** 6)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
