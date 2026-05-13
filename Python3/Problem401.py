import time


LIMIT = 10**15
MODULUS = 10**9


def squareSum(number, modulus=MODULUS):
    factors = [number, number + 1, 2 * number + 1]

    for divisor in (2, 3):
        for index, value in enumerate(factors):
            if value % divisor == 0:
                factors[index] = value // divisor
                break

    result = 1

    for value in factors:
        result = (result * (value % modulus)) % modulus

    return result


def sigma2Summatory(limit=LIMIT, modulus=MODULUS):
    total = 0
    divisor = 1

    while divisor <= limit:
        quotient = limit // divisor
        nextDivisor = limit // quotient
        squareBlock = (squareSum(nextDivisor, modulus) - squareSum(divisor - 1, modulus)) % modulus
        total = (total + (quotient % modulus) * squareBlock) % modulus
        divisor = nextDivisor + 1

    return total


def runTests():
    assert [sigma2Summatory(number) for number in range(1, 7)] == [1, 6, 16, 37, 63, 113]
    assert sigma2Summatory(1000) == 401382971


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sigma2Summatory()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
