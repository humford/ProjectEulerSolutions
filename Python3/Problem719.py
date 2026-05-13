import math
import time
from functools import lru_cache


def canSplitToSum(text, target):
    digits = [ord(char) - ord("0") for char in text]
    length = len(digits)

    suffixDigitSums = [0] * (length + 1)
    suffixValues = [0] * (length + 1)

    for index in range(length - 1, -1, -1):
        suffixDigitSums[index] = suffixDigitSums[index + 1] + digits[index]

    placeValue = 1
    for index in range(length - 1, -1, -1):
        suffixValues[index] = digits[index] * placeValue + suffixValues[index + 1]
        placeValue *= 10

    @lru_cache(maxsize=None)
    def search(index, remaining, pieceCount):
        if index == length:
            return remaining == 0 and pieceCount >= 2
        if remaining < suffixDigitSums[index] or remaining > suffixValues[index]:
            return False

        value = 0
        for end in range(index, length):
            value = 10 * value + digits[end]
            if value > remaining:
                break

            nextPieceCount = 2 if pieceCount else 1
            if search(end + 1, remaining - value, nextPieceCount):
                return True

        return False

    return search(0, target, 0)


def isSNumber(square):
    root = math.isqrt(square)
    return root * root == square and canSplitToSum(str(square), root)


def sNumberSum(limit):
    total = 0
    for root in range(1, math.isqrt(limit) + 1):
        # A split sum has the same residue modulo 9 as the original square.
        if root % 9 not in (0, 1):
            continue

        square = root * root
        if canSplitToSum(str(square), root):
            total += square

    return total


def runTests():
    assert isSNumber(81)
    assert isSNumber(6_724)
    assert isSNumber(8_281)
    assert isSNumber(9_801)
    assert not isSNumber(1)
    assert sNumberSum(10**4) == 41_333


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sNumberSum(10**12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
