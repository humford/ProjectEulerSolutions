import functools
import math
import time


def quotientWeightedSum(limit):
    total = 0
    start = 1

    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        total += quotient * (start + end) * (end - start + 1) // 2
        start = end + 1

    return total


def smallQuotientWeightedSums(limit):
    sigma = [0] * (limit + 1)

    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            sigma[multiple] += divisor

    sums = [0] * (limit + 1)
    for n in range(1, limit + 1):
        sums[n] = sums[n - 1] + sigma[n]

    return sums


def gaussianIntegerDivisorSum(limit):
    small_limit = math.isqrt(limit)
    small_sums = smallQuotientWeightedSums(small_limit)

    @functools.lru_cache(maxsize=None)
    def scaledSum(n):
        if n <= small_limit:
            return small_sums[n]
        return quotientWeightedSum(n)

    total = quotientWeightedSum(limit)

    for real_part in range(1, small_limit + 1):
        max_imaginary = math.isqrt(limit - real_part * real_part)

        for imaginary_part in range(1, max_imaginary + 1):
            if math.gcd(real_part, imaginary_part) == 1:
                norm = real_part * real_part + imaginary_part * imaginary_part
                total += 2 * real_part * scaledSum(limit // norm)

    return total


def runTests():
    assert quotientWeightedSum(5) == 21
    assert gaussianIntegerDivisorSum(5) == 35


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gaussianIntegerDivisorSum(10 ** 8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
