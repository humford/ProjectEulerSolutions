import time


TARGET = 10_000
MODULUS = 1_000_000_007
INVERSE_TWO = (MODULUS + 1) // 2


def signedCompositionValue(totalCards, bit, modulus=MODULUS):
    if bit == 0:
        if totalCards == 0:
            return 1
        return -pow(modulus - 2, totalCards - 1, modulus) % modulus

    blockSize = 1 << bit
    period = 2 * blockSize
    periodMask = period - 1
    values = [0] * (totalCards + 1)
    prefix = [0] * (totalCards + 1)
    values[0] = 1
    prefix[0] = 1

    for cards in range(1, totalCards + 1):
        value = 0
        start = 1
        while start <= cards:
            residue = start & periodMask
            if residue < blockSize:
                sign = 1
                end = start + (blockSize - residue) - 1
            else:
                sign = -1
                end = start + (period - residue) - 1

            if end > cards:
                end = cards

            low = cards - end
            high = cards - start
            if low == 0:
                rangeSum = prefix[high]
            else:
                rangeSum = prefix[high] - prefix[low - 1]
            value += sign * rangeSum
            start = end + 1

        values[cards] = value % modulus
        prefix[cards] = (prefix[cards - 1] + values[cards]) % modulus

    return values[totalCards]


def X(totalCards, modulus=MODULUS):
    if totalCards <= 0:
        return 0

    subsetCount = pow(2, totalCards - 1, modulus)
    total = 0
    bit = 0
    while (1 << bit) <= totalCards:
        signedValue = signedCompositionValue(totalCards, bit, modulus)
        bitContribution = (subsetCount - signedValue) * INVERSE_TWO % modulus
        total = (total + (1 << bit) * bitContribution) % modulus
        bit += 1

    return (total - (totalCards & 1)) % modulus


def solve():
    return X(TARGET)


def runTests():
    assert X(2) == 2
    assert X(4) == 14
    assert X(10) == 1418


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
