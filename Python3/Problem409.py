import time


LIMIT = 10_000_000
MODULUS = 1_000_000_007


def fallingBinomial(top, choose):
    numerator = 1
    denominator = 1
    top %= MODULUS

    for index in range(1, choose + 1):
        numerator = numerator * ((top - index + 1) % MODULUS) % MODULUS
        denominator = denominator * index % MODULUS

    return numerator * pow(denominator, MODULUS - 2, MODULUS) % MODULUS


def factorial(number):
    result = 1

    for value in range(1, number + 1):
        result = result * value % MODULUS

    return result


def winningPositions(n=LIMIT):
    vectorCount = pow(2, n, MODULUS)
    totalSubsets = fallingBinomial(vectorCount - 1, n)
    half = n // 2
    coefficient = fallingBinomial(pow(2, n - 1, MODULUS) - 1, half)

    if (n + half) % 2:
        coefficient = -coefficient % MODULUS

    unorderedWinning = (
        (vectorCount - 1)
        * pow(vectorCount, MODULUS - 2, MODULUS)
        * ((totalSubsets - coefficient) % MODULUS)
    ) % MODULUS

    return factorial(n) * unorderedWinning % MODULUS


def runTests():
    assert winningPositions(1) == 1
    assert winningPositions(2) == 6
    assert winningPositions(3) == 168
    assert winningPositions(5) == 19764360
    assert winningPositions(100) == 384777056


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningPositions()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
