import time


PRIME_COUNT = 904_961


def twoAdicValuation(number):
    exponent = 0
    while number and number % 2 == 0:
        exponent += 1
        number //= 2
    return exponent


def twoAdicFactorialValuation(limit):
    total = 0
    while limit:
        limit //= 2
        total += limit
    return total


def divisorPairCount(n):
    divisors = [divisor for divisor in range(1, n + 1) if n % divisor == 0]
    return sum(
        1
        for smaller in divisors
        for larger in divisors
        if smaller != larger and larger % smaller == 0
    )


def primorialPowerDivisorPairCount(m, n):
    factor = (n + 1) * (n + 2) // 2
    equalPairs = n + 1
    return factor**m - equalPairs**m


def divisorPairPower(m, n):
    if m % 2 == 0:
        return twoAdicValuation(primorialPowerDivisorPairCount(m, n))

    if n % 2 == 1:
        return m * (twoAdicValuation(n + 1) - 1)
    if n % 4 == 0:
        return twoAdicValuation(n) - 1
    return 0


def divisorPairPowerSum(n, m=PRIME_COUNT):
    oddContributionLimit = (n + 1) // 2
    divisibleByFourLimit = n // 4
    return (
        m * twoAdicFactorialValuation(oddContributionLimit)
        + divisibleByFourLimit
        + twoAdicFactorialValuation(divisibleByFourLimit)
    )


def runTests():
    assert divisorPairCount(6) == 5
    assert divisorPairPower(2, 1) == 0
    for m in (3, 5, 7):
        for n in range(1, 20):
            assert divisorPairPower(m, n) == twoAdicValuation(
                primorialPowerDivisorPairCount(m, n)
            )
    assert divisorPairPowerSum(8) == 2_714_886


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisorPairPowerSum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
