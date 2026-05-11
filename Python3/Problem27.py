def isPrime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2

    return True


def consecutivePrimeCount(a, b):
    n = 0
    while isPrime(n * n + a * n + b):
        n += 1
    return n


def bestQuadraticPrimeProduct(limit):
    best_count = 0
    best_product = 0

    for a in range(-limit + 1, limit):
        for b in range(-limit, limit + 1):
            count = consecutivePrimeCount(a, b)
            if count > best_count:
                best_count = count
                best_product = a * b

    return best_product


def runTests():
    assert consecutivePrimeCount(1, 41) == 40
    assert consecutivePrimeCount(-79, 1601) == 80


def solve():
    return bestQuadraticPrimeProduct(1000)


if __name__ == "__main__":
    runTests()
    print(solve())
