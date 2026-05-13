import time


TARGET_WIDTH = 10_000
PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19,
    23, 29, 31, 37, 41, 43, 47, 53,
]


def convolveWithDivisorChain(coefficients, exponent):
    output = []
    windowSum = 0

    for index in range(len(coefficients) + exponent):
        if index < len(coefficients):
            windowSum += coefficients[index]
        if index - exponent - 1 >= 0:
            windowSum -= coefficients[index - exponent - 1]
        output.append(windowSum)

    return output


def coefficientsForExponents(exponents):
    coefficients = [1]

    for exponent in exponents:
        coefficients = convolveWithDivisorChain(coefficients, exponent)

    return coefficients


def gFromExponents(exponents):
    return max(coefficientsForExponents(exponents))


def numberFromExponents(exponents):
    number = 1

    for prime, exponent in zip(PRIMES, exponents):
        number *= prime**exponent

    return number


def squareFreeUpperBound(target):
    exponents = []
    number = 1
    coefficients = [1]

    for prime in PRIMES:
        exponents.append(1)
        number *= prime
        coefficients = convolveWithDivisorChain(coefficients, 1)
        if max(coefficients) >= target:
            return number, exponents

    raise ValueError("not enough primes for square-free upper bound")


def smallestNumberForWidth(target):
    bestNumber, bestExponents = squareFreeUpperBound(target)
    searchPrimes = PRIMES[:len(bestExponents)]

    def search(primeIndex, maxExponent, number, coefficients, exponents):
        nonlocal bestNumber, bestExponents

        if max(coefficients) >= target:
            if number < bestNumber:
                bestNumber = number
                bestExponents = exponents
            return

        if primeIndex == len(searchPrimes):
            return

        prime = searchPrimes[primeIndex]
        nextNumber = number
        for exponent in range(1, maxExponent + 1):
            nextNumber *= prime
            if nextNumber >= bestNumber:
                break

            search(
                primeIndex + 1,
                exponent,
                nextNumber,
                convolveWithDivisorChain(coefficients, exponent),
                exponents + [exponent],
            )

    search(0, bestNumber.bit_length(), 1, [1], [])
    return bestNumber, bestExponents


def solve():
    return smallestNumberForWidth(TARGET_WIDTH)[0]


def runTests():
    assert gFromExponents([2, 1]) == 2
    assert gFromExponents([4, 2, 1, 1]) == 12
    answer, exponents = smallestNumberForWidth(TARGET_WIDTH)
    assert exponents == [4, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]
    assert gFromExponents(exponents) == 10130
    assert answer == 205702861096933200


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
