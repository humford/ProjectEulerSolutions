from decimal import Decimal, ROUND_HALF_UP, getcontext
import time


TARGET_N = 10**8


def primeSieve(limit):
    if limit < 2:
        return []

    size = (limit + 1) // 2
    isPrime = bytearray(b"\x01") * size
    isPrime[0] = 0

    root = int(limit**0.5)
    for p in range(3, root + 1, 2):
        if isPrime[p // 2]:
            start = p * p // 2
            isPrime[start:size:p] = b"\x00" * (((size - 1 - start) // p) + 1)

    primes = [2]
    primes.extend(2 * index + 1 for index in range(1, size) if isPrime[index])
    return primes


def totalOptimalScore(primes):
    score = 0
    activeGroups = [primes]
    depth = 0

    while activeGroups:
        nextGroups = []
        nextLengthThreshold = 1 << (depth + 1)

        for group in activeGroups:
            zeroCount = 0
            oneCount = 0
            zeroNext = []
            oneNext = []

            for prime in group:
                if (prime >> depth) & 1:
                    oneCount += 1
                    if prime >= nextLengthThreshold:
                        oneNext.append(prime)
                else:
                    zeroCount += 1
                    if prime >= nextLengthThreshold:
                        zeroNext.append(prime)

            score += max(zeroCount, oneCount)

            if zeroNext:
                nextGroups.append(zeroNext)
            if oneNext:
                nextGroups.append(oneNext)

        activeGroups = nextGroups
        depth += 1

    return score


def E(limit):
    primes = primeSieve(limit)
    return totalOptimalScore(primes), len(primes)


def formatExpectation(score, count, places=8):
    getcontext().prec = 40
    quant = Decimal(1).scaleb(-places)
    value = (Decimal(score) / Decimal(count)).quantize(quant, rounding=ROUND_HALF_UP)
    return format(value, "f")


def runTests():
    score10, count10 = E(10)
    assert score10 == 8
    assert count10 == 4
    assert formatExpectation(score10, count10, 1) == "2.0"

    score30, count30 = E(30)
    assert score30 == 29
    assert count30 == 10
    assert formatExpectation(score30, count30, 1) == "2.9"


def solve():
    score, count = E(TARGET_N)
    return formatExpectation(score, count, 8)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
