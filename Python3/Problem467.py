from array import array
import functools
import math
import time


MODULUS = 1_000_000_007


def _smallest_common_supersequence(a, b):
    @functools.lru_cache(None)
    def build(i, j):
        if i == len(a):
            return b[j:]
        if j == len(b):
            return a[i:]
        if a[i] == b[j]:
            return a[i] + build(i + 1, j + 1)

        left = a[i] + build(i + 1, j)
        right = b[j] + build(i, j + 1)
        if len(left) != len(right):
            return left if len(left) < len(right) else right
        return min(left, right)

    return build(0, 0)


def sieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if isPrime[number]:
            start = number * number
            isPrime[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)
    return isPrime


def digitalRoot(value):
    return 1 + (value - 1) % 9


def digitalRootSequences(count):
    limit = max(32, int(count * (math.log(count) + math.log(math.log(count))) + 32) if count >= 6 else 32)
    while True:
        isPrime = sieve(limit)
        primeRoots = []
        compositeRoots = []

        for value in range(2, limit + 1):
            if isPrime[value]:
                if len(primeRoots) < count:
                    primeRoots.append(digitalRoot(value))
            else:
                if len(compositeRoots) < count:
                    compositeRoots.append(digitalRoot(value))

            if len(primeRoots) == count and len(compositeRoots) == count:
                return primeRoots, compositeRoots

        limit *= 2


def supersequenceModulo(a, b, modulus):
    rows = len(a)
    columns = len(b)
    lengths = [array("H", [0]) * (columns + 1) for _ in range(rows + 1)]

    for column in range(columns, -1, -1):
        lengths[rows][column] = columns - column

    for rowIndex in range(rows - 1, -1, -1):
        row = lengths[rowIndex]
        nextRow = lengths[rowIndex + 1]
        row[columns] = rows - rowIndex
        digit = a[rowIndex]
        for column in range(columns - 1, -1, -1):
            if digit == b[column]:
                row[column] = nextRow[column + 1] + 1
            else:
                takeA = nextRow[column]
                takeB = row[column + 1]
                row[column] = (takeA if takeA < takeB else takeB) + 1

    row = 0
    column = 0
    value = 0
    while row < rows or column < columns:
        if row == rows:
            digit = b[column]
            column += 1
        elif column == columns:
            digit = a[row]
            row += 1
        elif a[row] == b[column]:
            digit = a[row]
            row += 1
            column += 1
        else:
            takeA = lengths[row + 1][column]
            takeB = lengths[row][column + 1]
            if takeA < takeB or (takeA == takeB and a[row] <= b[column]):
                digit = a[row]
                row += 1
            else:
                digit = b[column]
                column += 1

        value = (10 * value + digit) % modulus

    return value


def superinteger(count):
    primeRoots, compositeRoots = digitalRootSequences(count)
    return supersequenceModulo(primeRoots, compositeRoots, MODULUS)


def runTests():
    assert _smallest_common_supersequence("2357248152", "4689135679") == "2357246891352679"
    assert superinteger(10) == 2_357_246_891_352_679 % MODULUS
    assert superinteger(100) == 771_661_825


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = superinteger(10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
