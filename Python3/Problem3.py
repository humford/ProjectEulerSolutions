def largestPrimeFactor(n):
    factor = 2
    largest = 1

    while factor * factor <= n:
        while n % factor == 0:
            largest = factor
            n //= factor
        factor += 1 if factor == 2 else 2

    return max(largest, n)


def runTests():
    assert largestPrimeFactor(13195) == 29


def solve():
    return largestPrimeFactor(600851475143)


if __name__ == "__main__":
    runTests()
    print(solve())
