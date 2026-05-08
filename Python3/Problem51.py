import time
from itertools import combinations


def primeSieve(limit):
    primes = [True] * (limit + 1)
    primes[0] = False
    primes[1] = False

    for n in range(2, int(limit ** 0.5) + 1):
        if primes[n]:
            for multiple in range(n * n, limit + 1, n):
                primes[multiple] = False

    return primes


def replacementMasks(number):
    digits = str(number)

    for digit in sorted(set(digits)):
        positions = [i for i, d in enumerate(digits) if d == digit]
        for size in range(1, len(positions) + 1):
            for mask in combinations(positions, size):
                yield mask


def familyForMask(prime, mask, primes):
    digits = list(str(prime))
    family = []

    for replacement in "0123456789":
        if mask[0] == 0 and replacement == "0":
            continue

        candidate_digits = digits[:]
        for index in mask:
            candidate_digits[index] = replacement

        candidate = int("".join(candidate_digits))
        if primes[candidate]:
            family.append(candidate)

    return family


def smallestPrimeFamily(family_size, limit=1000000):
    primes = primeSieve(limit)

    for prime in range(2, limit + 1):
        if not primes[prime]:
            continue

        for mask in replacementMasks(prime):
            family = familyForMask(prime, mask, primes)
            if len(family) >= family_size:
                return prime, family

    raise ValueError("No prime family found below " + str(limit))


def runTests():
    small_primes = primeSieve(20)
    assert [n for n in range(20) if small_primes[n]] == [2, 3, 5, 7, 11, 13, 17, 19]

    primes = primeSieve(100000)
    assert familyForMask(56003, (2, 3), primes) == [
        56003,
        56113,
        56333,
        56443,
        56663,
        56773,
        56993,
    ]

    answer, family = smallestPrimeFamily(7, 100000)
    assert answer == 56003
    assert len(family) == 7


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer, family = smallestPrimeFamily(8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
