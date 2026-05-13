import time


def primesUpTo(limit):
    if limit >= 2:
        yield 2

    sieve = bytearray(b"\x01") * (limit // 2)

    for number in range(3, int(limit**0.5) + 1, 2):
        if sieve[number // 2]:
            start = number * number // 2
            sieve[start::number] = b"\x00" * (
                ((limit // 2 - 1) - start) // number + 1
            )

    for index in range(1, limit // 2):
        if sieve[index]:
            yield 2 * index + 1


def distinctPrimeFactors(number):
    factors = set()
    divisor = 2

    while divisor * divisor <= number:
        if number % divisor == 0:
            factors.add(divisor)

            while number % divisor == 0:
                number //= divisor

        divisor += 1 if divisor == 2 else 2

    if number > 1:
        factors.add(number)

    return factors


def s(n, limit):
    return sum(
        factor
        for factor in distinctPrimeFactors(n**15 + 1)
        if factor <= limit
    )


def rootsOfUnity(prime, order):
    if (prime - 1) % order:
        return [1]

    exponent = (prime - 1) // order
    base = 2

    while True:
        root = pow(base, exponent, prime)

        if root != 1:
            break

        base += 1

    roots = [1]
    value = 1

    for _ in range(1, order):
        value = value * root % prime
        roots.append(value)

    return roots


def fifteenthRootsOfMinusOne(prime):
    if prime == 2:
        return [1]

    roots = []
    seen = set()

    for thirdRoot in rootsOfUnity(prime, 3):
        for fifthRoot in rootsOfUnity(prime, 5):
            root = -(thirdRoot * fifthRoot) % prime

            if root and root not in seen:
                seen.add(root)
                roots.append(root)

    return roots


def totalPrimeFactorSum(maxN, maxPrime):
    total = 0

    for prime in primesUpTo(maxPrime):
        completePeriods, remainder = divmod(maxN, prime)
        roots = fifteenthRootsOfMinusOne(prime)
        rootCount = len(roots)
        partialPeriodCount = sum(1 for root in roots if root <= remainder)
        total += prime * (completePeriods * rootCount + partialPeriodCount)

    return total


def runTests():
    assert s(2, 10) == 3
    assert s(2, 1000) == 345
    assert s(10, 100) == 31
    assert s(10, 1000) == 483
    assert totalPrimeFactorSum(10, 100) == sum(s(n, 100) for n in range(1, 11))
    assert totalPrimeFactorSum(10, 1000) == sum(s(n, 1000) for n in range(1, 11))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totalPrimeFactorSum(10**11, 10**8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
