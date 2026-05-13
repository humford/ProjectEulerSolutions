import time


MODULUS = 1_000_000_007
TARGET_N = 10**8


def centralBinomial(n):
    factorial = 1
    factorialN = 1

    for value in range(1, 2 * n + 1):
        factorial = factorial * value % MODULUS
        if value == n:
            factorialN = factorial

    inverseFactorialN = pow(factorialN, MODULUS - 2, MODULUS)
    return factorial * inverseFactorialN % MODULUS * inverseFactorialN % MODULUS


def P(n):
    middle = centralBinomial(n)
    inverseNPlus1 = pow(n + 1, MODULUS - 2, MODULUS)
    inverseNPlus2 = pow(n + 2, MODULUS - 2, MODULUS)

    squareShape = middle * inverseNPlus1 % MODULUS
    nearSquareShape = (
        3 * middle % MODULUS
        * n % MODULUS
        * inverseNPlus1 % MODULUS
        * inverseNPlus2 % MODULUS
    )

    return (
        squareShape * squareShape
        + nearSquareShape * nearSquareShape
    ) % MODULUS


def solve():
    return P(TARGET_N)


def runTests():
    assert P(2) == 13
    assert P(10) == 45_265_702
    assert solve() == 877_789_135


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
