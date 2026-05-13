import math
import time
from array import array


LIMIT = 10 ** 14
MODULUS = 982451653


def maximumProductPartitionSumBrute(limit):
    total = 0

    for target in range(1, limit + 1):
        dp = [(-1, 0)] * (target + 1)
        dp[0] = (1, 0)

        for part in range(1, target + 1):
            for currentSum in range(target, part - 1, -1):
                previousProduct, previousCount = dp[currentSum - part]

                if previousProduct < 0:
                    continue

                candidate = (previousProduct * part, previousCount + 1)

                if candidate[0] > dp[currentSum][0]:
                    dp[currentSum] = candidate

        total += dp[target][0] * dp[target][1]

    return total


def baseSum(partCount):
    return partCount * (partCount + 3) // 2


def largestPartCount(limit):
    return (math.isqrt(8 * limit + 9) - 3) // 2


def modularInverses(limit, modulus):
    inverses = array("I", [0]) * (limit + 1)
    inverses[1] = 1

    for number in range(2, limit + 1):
        inverses[number] = ((modulus - modulus // number) * inverses[modulus % number]) % modulus

    return inverses


def maximumProductPartitionSum(limit=LIMIT, modulus=MODULUS):
    if limit <= 0:
        return 0

    total = 1
    if limit == 1:
        return total

    finalPartCount = largestPartCount(limit)
    inverses = modularInverses(finalPartCount + 3, modulus)
    inverseTwo = inverses[2]
    factorial = 2
    harmonicTail = (inverses[2] + inverses[3]) % modulus

    for partCount in range(1, finalPartCount):
        weightedFactorial = partCount * factorial % modulus
        total += (
            weightedFactorial
            * (partCount + 2)
            * harmonicTail
            + weightedFactorial * (partCount + 3) * inverseTwo
        )
        total %= modulus

        factorial = factorial * (partCount + 2) % modulus
        harmonicTail = (harmonicTail + inverses[partCount + 3]) % modulus

    remainder = limit - baseSum(finalPartCount)
    weightedFactorial = finalPartCount * factorial % modulus
    firstTerms = min(remainder, finalPartCount)

    if remainder >= finalPartCount:
        partialHarmonic = harmonicTail
    else:
        partialHarmonic = 0
        for denominator in range(
            finalPartCount + 2 - firstTerms, finalPartCount + 3
        ):
            partialHarmonic = (partialHarmonic + inverses[denominator]) % modulus

    total += weightedFactorial * (finalPartCount + 2) * partialHarmonic

    if remainder == finalPartCount + 1:
        total += weightedFactorial * (finalPartCount + 3) * inverseTwo

    return total % modulus


def runTests():
    assert maximumProductPartitionSumBrute(5) == 22
    assert maximumProductPartitionSumBrute(100) == 1683550844462
    assert maximumProductPartitionSum(5) == 22
    assert maximumProductPartitionSum(100) == 1683550844462 % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumProductPartitionSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
