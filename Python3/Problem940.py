import time


MODULUS = 1_123_581_313
TARGET = 50


def multiply(left, right):
    # Elements are a + b*x in Z[x] / (x^2 - x - 3).
    a, b = left
    c, d = right
    return (
        (a * c + 3 * b * d) % MODULUS,
        (a * d + b * c + b * d) % MODULUS,
    )


def power(base, exponent):
    result = (1, 0)

    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent //= 2

    return result


def fibonacciNumbers(limit):
    numbers = [0] * (limit + 1)
    numbers[1] = 1

    for index in range(1, limit):
        numbers[index + 1] = numbers[index] + numbers[index - 1]

    return numbers


def A(m, n):
    return multiply(power((1, 1), m), power((0, 1), n))[1]


def S(limit):
    fibs = fibonacciNumbers(limit)
    xPowers = {
        index: power((0, 1), fibs[index])
        for index in range(2, limit + 1)
    }
    yPowers = {
        index: power((1, 1), fibs[index])
        for index in range(2, limit + 1)
    }

    total = 0
    for i in range(2, limit + 1):
        for j in range(2, limit + 1):
            total = (total + multiply(yPowers[i], xPowers[j])[1]) % MODULUS

    return total


def solve():
    return S(TARGET)


def runTests():
    assert A(1, 1) == 2
    assert A(1, 2) == 5
    assert A(2, 1) == 7
    assert A(2, 2) == 16
    assert S(3) == 30
    assert S(5) == 10_396


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
