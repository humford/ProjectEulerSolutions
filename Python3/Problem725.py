import time


MODULUS = 10**16


def isDigitSumNumber(number):
    digits = [int(digit) for digit in str(number)]
    total = sum(digits)
    return any(2 * digit == total for digit in digits)


def witnessDigitContribution(maxDigits, witnessDigit):
    targetSum = 2 * witnessDigit
    counts = [[0, 0] for _ in range(targetSum + 1)]
    sums = [[0, 0] for _ in range(targetSum + 1)]

    for firstDigit in range(1, 10):
        if firstDigit > targetSum:
            continue
        seenWitness = 1 if firstDigit == witnessDigit else 0
        counts[firstDigit][seenWitness] += 1
        sums[firstDigit][seenWitness] += firstDigit

    total = sums[targetSum][1] % MODULUS

    for _ in range(2, maxDigits + 1):
        nextCounts = [[0, 0] for _ in range(targetSum + 1)]
        nextSums = [[0, 0] for _ in range(targetSum + 1)]

        for digitSum in range(targetSum + 1):
            for seenWitness in range(2):
                count = counts[digitSum][seenWitness]
                valueSum = sums[digitSum][seenWitness]
                if count == 0 and valueSum == 0:
                    continue

                for digit in range(10):
                    nextDigitSum = digitSum + digit
                    if nextDigitSum > targetSum:
                        break

                    nextSeenWitness = seenWitness or digit == witnessDigit
                    nextCounts[nextDigitSum][nextSeenWitness] = (
                        nextCounts[nextDigitSum][nextSeenWitness] + count
                    ) % MODULUS
                    nextSums[nextDigitSum][nextSeenWitness] = (
                        nextSums[nextDigitSum][nextSeenWitness]
                        + 10 * valueSum
                        + digit * count
                    ) % MODULUS

        counts = nextCounts
        sums = nextSums
        total = (total + sums[targetSum][1]) % MODULUS

    return total


def digitSumNumberPrefix(digits):
    total = 0
    for witnessDigit in range(10):
        total += witnessDigitContribution(digits, witnessDigit)
    return total % MODULUS


def runTests():
    assert isDigitSumNumber(352)
    assert isDigitSumNumber(3_003)
    assert isDigitSumNumber(32_812)
    assert digitSumNumberPrefix(3) == 63_270
    assert digitSumNumberPrefix(7) == 85_499_991_450


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = digitSumNumberPrefix(2_020)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
