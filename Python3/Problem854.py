import time


MOD = 1_234_567_891


def fibonacciPair(n):
    if n == 0:
        return 0, 1

    a, b = fibonacciPair(n // 2)
    c = a * (2 * b - a)
    d = a * a + b * b

    if n % 2:
        return d, c + d
    return c, d


def fibonacci(n):
    return fibonacciPair(n)[0]


def lucas(n):
    fn, fn1 = fibonacciPair(n)
    return 2 * fn1 - fn


def M(period):
    if period == 3:
        return 2
    if period % 2:
        return 1

    half = period // 2
    if half < 3:
        return 1
    if half % 2 == 0:
        return fibonacci(half)
    return lucas(half)


def PSmall(limit):
    product = 1
    for period in range(1, limit + 1):
        product *= M(period)
    return product


def P(limit, modulus=MOD):
    result = 2 if limit >= 3 else 1
    maxHalf = limit // 2

    fibPrevious, fibCurrent = 0, 1
    lucasPrevious, lucasCurrent = 2 % modulus, 1

    for half in range(2, maxHalf + 1):
        fibPrevious, fibCurrent = fibCurrent, (fibPrevious + fibCurrent) % modulus
        lucasPrevious, lucasCurrent = lucasCurrent, (lucasPrevious + lucasCurrent) % modulus

        if half < 3:
            continue
        if half % 2 == 0:
            result = result * fibCurrent % modulus
        else:
            result = result * lucasCurrent % modulus

    return result % modulus


def runTests():
    assert M(18) == 76
    assert PSmall(10) == 264


def solve():
    return P(1_000_000)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
