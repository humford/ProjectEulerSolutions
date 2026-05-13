from functools import lru_cache
import time


TARGET_N = 7**17


def isLosingByPattern(a, b):
    if a > b:
        a, b = b, a

    modulus = 1 << a.bit_length()
    return b % modulus == modulus - 1


@lru_cache(maxsize=None)
def bruteIsLosing(a, b):
    if a > b:
        a, b = b, a

    small = a
    for takeA in range(small + 1):
        takeB = small - takeA
        if takeA == a or takeB == b:
            continue
        nextA = a - takeA
        nextB = b - takeB
        if nextA <= 0 or nextB <= 0:
            continue
        if bruteIsLosing(nextA, nextB):
            return False

    return True


def bruteL(limit):
    count = 0

    for a in range(1, limit + 1):
        for b in range(1, limit + 1):
            if bruteIsLosing(a, b):
                count += 1

    return count


def L(limit):
    unorderedCount = 0
    bitLength = 1

    while 1 << (bitLength - 1) <= limit:
        low = 1 << (bitLength - 1)
        high = min(limit, (1 << bitLength) - 1)
        aCount = high - low + 1

        modulus = 1 << bitLength
        residue = modulus - 1
        if limit >= residue:
            bCount = (limit - residue) // modulus + 1
        else:
            bCount = 0

        unorderedCount += aCount * bCount
        bitLength += 1

    diagonalCount = (limit + 1).bit_length() - 1
    return 2 * unorderedCount - diagonalCount


def solve():
    return L(TARGET_N)


def runTests():
    assert all(
        bruteIsLosing(a, b) == isLosingByPattern(a, b)
        for a in range(1, 16)
        for b in range(1, 16)
    )
    assert bruteL(7) == 21
    assert L(7) == 21
    assert L(7**2) == 221
    assert solve() == 10784223938983273


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
