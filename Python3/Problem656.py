import itertools
import math
import time


LAST_DIGITS_MODULUS = 10 ** 15


def squareRootContinuedFractionTail(radicand):
    root = math.isqrt(radicand)
    if root * root == radicand:
        raise ValueError("radicand must not be a perfect square")

    m = 0
    d = 1
    a = root
    while True:
        m = d * a - m
        d = (radicand - m * m) // d
        a = (root + m) // d
        yield a


def palindromicSequenceIndexes(count, radicand):
    indexes = []
    qBeforePrevious = 0
    qPrevious = 1

    for convergentIndex, partial in enumerate(
        squareRootContinuedFractionTail(radicand),
        start=1,
    ):
        if convergentIndex % 2 == 1:
            for multiplier in range(1, partial + 1):
                indexes.append(qBeforePrevious + multiplier * qPrevious)
                if len(indexes) == count:
                    return indexes

        qBeforePrevious, qPrevious = (
            qPrevious,
            partial * qPrevious + qBeforePrevious,
        )

    return indexes


def palindromicSequenceIndexSum(count, radicand):
    return sum(palindromicSequenceIndexes(count, radicand))


def palindromicSequenceTotal(limit):
    total = 0
    for radicand in range(2, limit + 1):
        root = math.isqrt(radicand)
        if root * root != radicand:
            total += palindromicSequenceIndexSum(100, radicand)
    return total % LAST_DIGITS_MODULUS


def beattyDifference(radicand, index):
    return (
        math.isqrt(radicand * index * index)
        - math.isqrt(radicand * (index - 1) * (index - 1))
    )


def isPalindromicPrefix(radicand, length):
    return all(
        beattyDifference(radicand, index)
        == beattyDifference(radicand, length + 1 - index)
        for index in range(1, length // 2 + 1)
    )


def brutePalindromicSequenceIndexes(count, radicand):
    indexes = []
    for length in itertools.count(1):
        if isPalindromicPrefix(radicand, length):
            indexes.append(length)
            if len(indexes) == count:
                return indexes


def runTests():
    firstTwenty = [
        1,
        3,
        5,
        7,
        44,
        81,
        118,
        273,
        3_158,
        9_201,
        15_244,
        21_287,
        133_765,
        246_243,
        358_721,
        829_920,
        9_600_319,
        27_971_037,
        46_341_755,
        64_712_473,
    ]
    assert palindromicSequenceIndexes(20, 31) == firstTwenty
    assert palindromicSequenceIndexSum(20, 31) == 150_243_655

    for radicand in [2, 3, 5, 31]:
        assert palindromicSequenceIndexes(
            8,
            radicand,
        ) == brutePalindromicSequenceIndexes(8, radicand)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = palindromicSequenceTotal(1_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
