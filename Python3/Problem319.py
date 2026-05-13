import time


LIMIT = 10**10
MODULUS = 10**9
SIEVE_LIMIT = 2_000_000


def mobiusPrefix(limit):
    mobius = [1] * (limit + 1)
    mobius[0] = 0
    primes = []
    composite = bytearray(limit + 1)

    for number in range(2, limit + 1):
        if not composite[number]:
            primes.append(number)
            mobius[number] = -1

        for prime in primes:
            multiple = number * prime
            if multiple > limit:
                break

            composite[multiple] = 1

            if number % prime == 0:
                mobius[multiple] = 0
                break

            mobius[multiple] = -mobius[number]

    prefix = [0] * (limit + 1)
    running = 0

    for number in range(1, limit + 1):
        running += mobius[number]
        prefix[number] = running

    return prefix


def powerSumDifference(exponent, modulus):
    if modulus is None:
        sum3 = (3 ** (exponent + 1) - 3) // 2
        sum2 = 2 ** (exponent + 1) - 2
        return sum3 - sum2 - exponent

    sum3 = ((pow(3, exponent + 1, 2 * modulus) - 3) % (2 * modulus)) // 2
    sum2 = (pow(2, exponent + 1, modulus) - 2) % modulus

    return (sum3 - sum2 - exponent) % modulus


def boundedSequenceCount(limit=LIMIT, modulus=MODULUS, sieveLimit=SIEVE_LIMIT):
    sieveLimit = min(sieveLimit, limit)
    prefix = mobiusPrefix(sieveLimit)
    cache = {}

    def mertens(number):
        if number <= sieveLimit:
            return prefix[number]

        if number in cache:
            return cache[number]

        total = 1
        divisor = 2

        while divisor <= number:
            quotient = number // divisor
            nextDivisor = number // quotient
            total -= (nextDivisor - divisor + 1) * mertens(quotient)
            divisor = nextDivisor + 1

        cache[number] = total
        return total

    total = 1
    divisor = 1

    while divisor <= limit:
        quotient = limit // divisor
        nextDivisor = limit // quotient
        coefficient = mertens(nextDivisor) - mertens(divisor - 1)
        contribution = coefficient * powerSumDifference(quotient, modulus)

        if modulus is None:
            total += contribution
        else:
            total = (total + contribution) % modulus

        divisor = nextDivisor + 1

    return total


def runTests():
    assert boundedSequenceCount(2, None, 10) == 5
    assert boundedSequenceCount(5, None, 10) == 293
    assert boundedSequenceCount(10, None, 20) == 86195
    assert boundedSequenceCount(20, None, 20) == 5227991891


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = boundedSequenceCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
