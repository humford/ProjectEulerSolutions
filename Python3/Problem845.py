from math import isqrt
import time


def primeTable(limit):
    isPrime = [True] * (limit + 1)
    if limit >= 0:
        isPrime[0] = False
    if limit >= 1:
        isPrime[1] = False

    for p in range(2, isqrt(limit) + 1):
        if isPrime[p]:
            for multiple in range(p * p, limit + 1, p):
                isPrime[multiple] = False

    return isPrime


def digitSumCounts(maxLength):
    maxSum = 9 * maxLength
    counts = [[0] * (maxSum + 1) for _ in range(maxLength + 1)]
    counts[0][0] = 1

    for length in range(1, maxLength + 1):
        for total in range(9 * length + 1):
            counts[length][total] = sum(
                counts[length - 1][total - digit]
                for digit in range(10)
                if total >= digit
            )

    return counts


def countWithLength(length, counts, isPrime):
    if length <= 0:
        return 0

    total = 0
    remaining = length - 1
    for firstDigit in range(1, 10):
        for tailSum in range(9 * remaining + 1):
            if isPrime[firstDigit + tailSum]:
                total += counts[remaining][tailSum]

    return total


def kthNumberWithLength(length, k, counts, isPrime):
    digits = []
    prefixSum = 0

    for position in range(length):
        remaining = length - position - 1
        startDigit = 1 if position == 0 else 0

        for digit in range(startDigit, 10):
            candidateSum = prefixSum + digit
            count = 0
            for tailSum in range(9 * remaining + 1):
                if isPrime[candidateSum + tailSum]:
                    count += counts[remaining][tailSum]

            if k > count:
                k -= count
            else:
                digits.append(str(digit))
                prefixSum += digit
                break

    return int("".join(digits))


def D(n):
    maxLength = 25
    isPrime = primeTable(9 * maxLength)
    counts = digitSumCounts(maxLength)
    remaining = n

    for length in range(1, maxLength + 1):
        count = countWithLength(length, counts, isPrime)
        if remaining > count:
            remaining -= count
        else:
            return kthNumberWithLength(length, remaining, counts, isPrime)

    raise RuntimeError("maxLength too small")


def runTests():
    assert D(61) == 157
    assert D(10**8) == 403_539_364


def solve():
    return D(10**16)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
