def sumOfSquares(n):
    s = 0
    for i in range(1, n + 1):
        s += (i ** 2)
    return s


def squareOfSum(n):
    s = 0
    for i in range(1, n + 1):
        s += i
    return s ** 2


def sumSquareDifference(n):
    return squareOfSum(n) - sumOfSquares(n)


print(sumSquareDifference(100))
