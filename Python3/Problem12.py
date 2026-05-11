def numberOfDivisors(n):
    count = 1
    factor = 2

    while factor * factor <= n:
        exponent = 0
        while n % factor == 0:
            exponent += 1
            n //= factor
        if exponent:
            count *= exponent + 1
        factor += 1 if factor == 2 else 2

    if n > 1:
        count *= 2

    return count


def triangleNumber(index):
    return index * (index + 1) // 2


def firstTriangleWithDivisorsOver(limit):
    index = 1
    while True:
        triangle = triangleNumber(index)
        if numberOfDivisors(triangle) > limit:
            return triangle
        index += 1


def runTests():
    assert numberOfDivisors(28) == 6
    assert firstTriangleWithDivisorsOver(5) == 28


def solve():
    return firstTriangleWithDivisorsOver(500)


if __name__ == "__main__":
    runTests()
    print(solve())
