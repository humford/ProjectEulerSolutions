import fractions
import math
import time


EULER_GAMMA = 0.5772156649015328606065120900824024310421


def harmonicExact(n):
    total = fractions.Fraction(0, 1)
    for denominator in range(1, n + 1):
        total += fractions.Fraction(1, denominator)
    return total


def harmonicSquareExact(n):
    total = fractions.Fraction(0, 1)
    for denominator in range(1, n + 1):
        total += fractions.Fraction(1, denominator * denominator)
    return total


def expectedDroneDistanceExact(packages):
    harmonic = harmonicExact(packages)
    harmonicSquare = harmonicSquareExact(packages)
    return fractions.Fraction(packages, 2) * (
        harmonic * harmonic + harmonicSquare
    )


def harmonicAsymptotic(n):
    inverse = 1.0 / n
    inverse2 = inverse * inverse
    inverse4 = inverse2 * inverse2
    inverse6 = inverse4 * inverse2
    return (
        math.log(n)
        + EULER_GAMMA
        + 0.5 * inverse
        - inverse2 / 12.0
        + inverse4 / 120.0
        - inverse6 / 252.0
    )


def harmonicSquareAsymptotic(n):
    inverse = 1.0 / n
    inverse2 = inverse * inverse
    inverse3 = inverse2 * inverse
    inverse5 = inverse3 * inverse2
    inverse7 = inverse5 * inverse2
    return (
        math.pi * math.pi / 6.0
        - inverse
        + 0.5 * inverse2
        - inverse3 / 6.0
        + inverse5 / 30.0
        - inverse7 / 42.0
    )


def expectedDroneDistance(packages):
    if packages <= 2_000:
        return float(expectedDroneDistanceExact(packages))

    harmonic = harmonicAsymptotic(packages)
    harmonicSquare = harmonicSquareAsymptotic(packages)
    return 0.5 * packages * (harmonic * harmonic + harmonicSquare)


def roundedExpectedDroneDistance(packages):
    return math.floor(expectedDroneDistance(packages) + 0.5)


def runTests():
    assert expectedDroneDistanceExact(2) == fractions.Fraction(7, 2)
    assert expectedDroneDistanceExact(5) == fractions.Fraction(12_019, 720)
    assert abs(expectedDroneDistance(100) - 1427.193470) < 1e-6


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedExpectedDroneDistance(10**8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
