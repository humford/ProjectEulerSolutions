import time


LIMIT = 10**10
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


def distinctLineCount(limit=LIMIT, sieveLimit=SIEVE_LIMIT):
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

    total = 0
    divisor = 1

    while divisor <= limit:
        quotient = limit // divisor
        nextDivisor = limit // quotient
        coefficient = mertens(nextDivisor) - mertens(divisor - 1)
        total += coefficient * (quotient**3 + 3 * quotient**2 + 3 * quotient)
        divisor = nextDivisor + 1

    return total


def answerFor(limit=LIMIT):
    count = str(distinctLineCount(limit))
    return count[:9] + count[-9:]


def bruteDistinctLineCount(limit):
    count = 0

    for a in range(limit + 1):
        for b in range(limit + 1):
            for c in range(limit + 1):
                if a == b == c == 0:
                    continue

                x, y = a, b
                while y:
                    x, y = y, x % y

                z = c
                while z:
                    x, z = z, x % z

                if x == 1:
                    count += 1

    return count


def runTests():
    assert distinctLineCount(1, 1) == 7
    assert distinctLineCount(2, 2) == 19
    assert distinctLineCount(20, 20) == bruteDistinctLineCount(20)
    assert distinctLineCount(1_000_000) == 831909254469114121


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = answerFor()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
