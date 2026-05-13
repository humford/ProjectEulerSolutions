import math
import time


MOD = 1_000_000_007


def oddPrimesUpTo(limit):
    if limit < 3:
        return []

    sieve = bytearray(limit // 2 + 1)
    for candidate in range(3, math.isqrt(limit) + 1, 2):
        if sieve[candidate // 2]:
            continue
        startIndex = candidate * candidate // 2
        sieve[startIndex::candidate] = b"\x01" * (
            ((len(sieve) - startIndex - 1) // candidate) + 1
        )

    return [candidate for candidate in range(3, limit + 1, 2) if not sieve[candidate // 2]]


def lcmRangeMod(limit, modulus=MOD):
    if limit <= 1:
        return 1 % modulus

    result = 1
    power = 2
    while power <= limit:
        result = result * 2 % modulus
        power *= 2

    sqrtLimit = math.isqrt(limit)
    basePrimes = oddPrimesUpTo(sqrtLimit)

    oddCandidatesPerSegment = 1_000_000
    span = 2 * oddCandidatesPerSegment
    low = 3
    while low <= limit:
        high = min(limit + 1, low + span)
        count = (high - low + 1) // 2
        segment = bytearray(count)

        for prime in basePrimes:
            if prime * prime >= high:
                break
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)
            if start % 2 == 0:
                start += prime
            if start >= high:
                continue
            index = (start - low) // 2
            segment[index::prime] = b"\x01" * (((count - index - 1) // prime) + 1)

        value = low
        for composite in segment:
            if not composite:
                result = result * value % modulus
                if value <= sqrtLimit:
                    primePower = value * value
                    while primePower <= limit:
                        result = result * value % modulus
                        primePower *= value
            value += 2

        low = high if high % 2 else high + 1

    return result


def f(k):
    return 2 * lcmRangeMod(k) % MOD


def runTests():
    assert f(3) == 12
    assert f(30) == 179_092_994


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f(10 ** 8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
