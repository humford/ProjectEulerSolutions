from math import comb


def countCombinationsGreaterThan(nLimit, threshold):
    count = 0
    for n in range(1, nLimit + 1):
        for r in range(1, n):
            if comb(n, r) > threshold:
                count += 1
    return count


def runTests():
    assert comb(23, 10) > 1000000
    assert comb(22, 10) < 1000000


def solve():
    return countCombinationsGreaterThan(100, 1000000)


if __name__ == "__main__":
    runTests()
    print(solve())
