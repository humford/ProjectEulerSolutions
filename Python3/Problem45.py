from math import isqrt


def triangleNumber(n):
    return n * (n + 1) // 2


def pentagonalNumber(n):
    return n * (3 * n - 1) // 2


def hexagonalNumber(n):
    return n * (2 * n - 1)


def isPentagonal(n):
    root = isqrt(24 * n + 1)
    return root * root == 24 * n + 1 and (root + 1) % 6 == 0


def isHexagonal(n):
    root = isqrt(8 * n + 1)
    return root * root == 8 * n + 1 and (root + 1) % 4 == 0


def nextTrianglePentagonalHexagonal(afterTriangleIndex):
    index = afterTriangleIndex + 1
    while True:
        value = triangleNumber(index)
        if isPentagonal(value) and isHexagonal(value):
            return value
        index += 1


def runTests():
    assert triangleNumber(285) == 40755
    assert pentagonalNumber(165) == 40755
    assert hexagonalNumber(143) == 40755
    assert isPentagonal(40755)
    assert isHexagonal(40755)


def solve():
    return nextTrianglePentagonalHexagonal(285)


if __name__ == "__main__":
    runTests()
    print(solve())
