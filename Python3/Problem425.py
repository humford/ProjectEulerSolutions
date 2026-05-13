import heapq
import time
from array import array


LIMIT = 10**7


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[:2] = b"\x00\x00"

    for number in range(2, int(limit**0.5) + 1):
        if isPrime[number]:
            start = number * number
            isPrime[start : limit + 1 : number] = b"\x00" * (
                ((limit - start) // number) + 1
            )

    return isPrime


def connectedPrimes(prime, limit, isPrime):
    digits = str(prime)
    seen = set()

    for index, current in enumerate(digits):
        for replacement in "0123456789":
            if replacement == current or (index == 0 and replacement == "0"):
                continue

            candidate = int(digits[:index] + replacement + digits[index + 1 :])

            if candidate <= limit and isPrime[candidate] and candidate not in seen:
                seen.add(candidate)
                yield candidate

    if len(digits) > 1:
        candidate = int(digits[1:])

        if candidate <= limit and isPrime[candidate] and candidate not in seen:
            seen.add(candidate)
            yield candidate

    place = 10 ** len(digits)

    for leading in range(1, 10):
        candidate = leading * place + prime

        if candidate <= limit and isPrime[candidate] and candidate not in seen:
            seen.add(candidate)
            yield candidate


def nonRelativePrimeSum(limit=LIMIT):
    isPrime = primeSieve(limit)
    primes = [number for number in range(2, limit + 1) if isPrime[number]]
    infinity = limit + 1
    distance = array("I", [infinity]) * (limit + 1)
    distance[2] = 2
    queue = [(2, 2)]

    while queue:
        currentMaximum, prime = heapq.heappop(queue)

        if currentMaximum != distance[prime]:
            continue

        for candidate in connectedPrimes(prime, limit, isPrime):
            nextMaximum = max(currentMaximum, candidate)

            if nextMaximum < distance[candidate]:
                distance[candidate] = nextMaximum
                heapq.heappush(queue, (nextMaximum, candidate))

    return sum(prime for prime in primes if distance[prime] > prime)


def runTests():
    assert nonRelativePrimeSum(10**3) == 431
    assert nonRelativePrimeSum(10**4) == 78728


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nonRelativePrimeSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
