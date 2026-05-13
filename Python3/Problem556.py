from array import array
import math
import time


def gaussianMobiusByNorm(limit):
    smallestPrimeFactor = array("I", [0]) * (limit + 1)
    for number in range(2, limit + 1):
        if smallestPrimeFactor[number] != 0:
            continue

        smallestPrimeFactor[number] = number
        if number * number <= limit:
            for multiple in range(number * number, limit + 1, number):
                if smallestPrimeFactor[multiple] == 0:
                    smallestPrimeFactor[multiple] = number

    mobius = array("i", [0]) * (limit + 1)
    mobius[1] = 1
    for number in range(2, limit + 1):
        prime = smallestPrimeFactor[number]
        rest = number // prime
        exponent = 1
        while rest % prime == 0:
            rest //= prime
            exponent += 1

        if prime == 2:
            coefficient = -1 if exponent == 1 else 0
        elif prime % 4 == 1:
            coefficient = -2 if exponent == 1 else (1 if exponent == 2 else 0)
        else:
            coefficient = -1 if exponent == 2 else 0

        if coefficient:
            mobius[number] = mobius[rest] * coefficient

    return mobius


def properGaussianCount(limit):
    root = math.isqrt(limit)
    total = 0
    for realPart in range(1, root + 1):
        total += math.isqrt(limit - realPart * realPart) + 1
    return total


def properGaussianCountTable(limit):
    counts = array("I", [0]) * (limit + 1)
    root = math.isqrt(limit)
    for realPart in range(1, root + 1):
        realSquare = realPart * realPart
        maxImaginary = math.isqrt(limit - realSquare)
        for imaginaryPart in range(maxImaginary + 1):
            counts[realSquare + imaginaryPart * imaginaryPart] += 1

    running = 0
    for value in range(limit + 1):
        running += counts[value]
        counts[value] = running
    return counts


def squarefreeGaussianCount(limit):
    normLimit = math.isqrt(limit)
    mobius = gaussianMobiusByNorm(normLimit)

    split = min(5_000, normLimit)
    tableLimit = limit // ((split + 1) * (split + 1)) if split < normLimit else 0
    smallCounts = properGaussianCountTable(tableLimit)

    total = 0
    for norm in range(1, normLimit + 1):
        coefficient = mobius[norm]
        if coefficient == 0:
            continue

        reducedLimit = limit // (norm * norm)
        if norm <= split:
            count = properGaussianCount(reducedLimit)
        else:
            count = smallCounts[reducedLimit]
        total += coefficient * count

    return total


def runTests():
    assert squarefreeGaussianCount(10) == 7
    assert squarefreeGaussianCount(10 ** 2) == 54
    assert squarefreeGaussianCount(10 ** 4) == 5_218
    assert squarefreeGaussianCount(10 ** 8) == 52_126_906


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squarefreeGaussianCount(10 ** 14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
