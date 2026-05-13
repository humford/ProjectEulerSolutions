import math
import time


SEARCH_LIMIT = 10**9
TARGET_COUNT = 4
TARGET_TERMS = 5


def palindromes(limit):
    values = set()
    maxPrefix = 10 ** ((len(str(limit)) + 1) // 2)

    for prefix in range(1, maxPrefix):
        text = str(prefix)

        odd = int(text + text[-2::-1])
        if odd <= limit:
            values.add(odd)

        even = int(text + text[::-1])
        if even <= limit:
            values.add(even)

    return values


def representationCounts(limit):
    palindromeSet = palindromes(limit)
    counts = {}
    squares = [number * number for number in range(2, math.isqrt(limit) + 1)]
    cube = 8
    base = 2

    while cube < limit:
        for square in squares:
            value = square + cube

            if value > limit:
                break

            if value in palindromeSet:
                counts[value] = min(TARGET_COUNT + 1, counts.get(value, 0) + 1)

        base += 1
        cube = base * base * base

    return counts


def representationCount(number):
    total = 0
    cubeBase = 2
    cube = 8

    while cube < number:
        square = number - cube
        root = math.isqrt(square)

        if root > 1 and root * root == square:
            total += 1

        cubeBase += 1
        cube = cubeBase * cubeBase * cubeBase

    return total


def palindromeSquareCubeSum():
    counts = representationCounts(SEARCH_LIMIT)
    matches = sorted(value for value, count in counts.items() if count == TARGET_COUNT)
    return sum(matches[:TARGET_TERMS])


def runTests():
    assert representationCount(5229225) == 4


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = palindromeSquareCubeSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
