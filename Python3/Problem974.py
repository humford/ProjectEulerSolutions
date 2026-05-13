from functools import lru_cache
import time


TARGET = 10**16
DIGITS = (1, 3, 5, 7, 9)
DIGIT_BITS = {digit: 1 << index for index, digit in enumerate(DIGITS)}
ALL_ODD_MASK = (1 << len(DIGITS)) - 1


def countWithLength(length):
    @lru_cache(maxsize=None)
    def count(position, remainder7, remainder3, parityMask):
        if position == length:
            return int(
                remainder7 == 0
                and remainder3 == 0
                and parityMask == ALL_ODD_MASK
            )

        allowedDigits = (5,) if position == length - 1 else DIGITS
        total = 0
        for digit in allowedDigits:
            total += count(
                position + 1,
                (10 * remainder7 + digit) % 7,
                (remainder3 + digit) % 3,
                parityMask ^ DIGIT_BITS[digit],
            )

        return total

    return count(0, 0, 0, 0)


def countCompletions(length):
    @lru_cache(maxsize=None)
    def count(position, remainder7, remainder3, parityMask):
        if position == length:
            return int(
                remainder7 == 0
                and remainder3 == 0
                and parityMask == ALL_ODD_MASK
            )

        allowedDigits = (5,) if position == length - 1 else DIGITS
        total = 0
        for digit in allowedDigits:
            total += count(
                position + 1,
                (10 * remainder7 + digit) % 7,
                (remainder3 + digit) % 3,
                parityMask ^ DIGIT_BITS[digit],
            )

        return total

    return count


def theta(index):
    length = 1
    remainingIndex = index

    while True:
        lengthCount = countWithLength(length)
        if remainingIndex > lengthCount:
            remainingIndex -= lengthCount
            length += 1
        else:
            break

    count = countCompletions(length)
    digits = []
    remainder7 = 0
    remainder3 = 0
    parityMask = 0

    for position in range(length):
        allowedDigits = (5,) if position == length - 1 else DIGITS
        for digit in allowedDigits:
            nextRemainder7 = (10 * remainder7 + digit) % 7
            nextRemainder3 = (remainder3 + digit) % 3
            nextParityMask = parityMask ^ DIGIT_BITS[digit]
            blockSize = count(
                position + 1,
                nextRemainder7,
                nextRemainder3,
                nextParityMask,
            )
            if remainingIndex > blockSize:
                remainingIndex -= blockSize
            else:
                digits.append(str(digit))
                remainder7 = nextRemainder7
                remainder3 = nextRemainder3
                parityMask = nextParityMask
                break

    return int("".join(digits))


def solve():
    return theta(TARGET)


def runTests():
    assert theta(1) == 1_117_935
    assert theta(10**3) == 11_137_955_115


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
