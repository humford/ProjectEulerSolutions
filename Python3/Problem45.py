import math


def triangleNumber(n):
    return n * (n + 1) / 2


def pentagonalNumber(n):
    return n * (3 * n - 1) / 2


def hexagonalNumber(n):
    return n * (2 * n - 1)


def testPentagonal(n):
    n = float(n)
    n = (math.sqrt(24 * n + 1) + 1) / 6
    print(n)
    return n.is_integer()


def testHexagonal(n):
    n = float(n)
    n = (math.sqrt(8 * n + 1) + 1) / 4
    print(n)
    return n.is_integer()


def findConversion(T):
    e = False
    while not e:
        T += 1
        test = triangleNumber(T)
        e = (testHexagonal(test) and testPentagonal(test))
    return triangleNumber(T)


print(findConversion(285))
