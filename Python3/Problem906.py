from fractions import Fraction
from math import comb
import time


TARGET_N = 20_000


def kahanAdd(total, compensation, value):
    adjusted = value - compensation
    nextTotal = total + adjusted
    return nextTotal, (nextTotal - total) - adjusted


def agreementProbability(n, tailEpsilon=1e-16):
    alternativesAbove = n - 1
    total = 0.0
    totalCompensation = 0.0

    for firstAbove in range(alternativesAbove + 1):
        avoidanceProbability = 1.0
        inner = 0.0
        innerCompensation = 0.0
        maxSecondAbove = alternativesAbove - firstAbove

        for secondAbove in range(maxSecondAbove + 1):
            term = avoidanceProbability / (firstAbove + secondAbove + 1)
            inner, innerCompensation = kahanAdd(inner, innerCompensation, term)

            if secondAbove == maxSecondAbove:
                break

            nextProbability = (
                avoidanceProbability
                * (alternativesAbove - firstAbove - secondAbove)
                / (alternativesAbove - secondAbove)
            )
            nextDenominator = firstAbove + secondAbove + 2
            remainingDenominator = alternativesAbove - secondAbove - 1

            if remainingDenominator > 0:
                ratioBound = (
                    (alternativesAbove - firstAbove - secondAbove - 1)
                    / remainingDenominator
                )
            else:
                ratioBound = 0.0

            if ratioBound < 1.0:
                nextTerm = nextProbability / nextDenominator
                if ratioBound > 0:
                    tailBound = nextTerm / (1.0 - ratioBound)
                else:
                    tailBound = nextTerm
                if tailBound < tailEpsilon:
                    break

            avoidanceProbability = nextProbability

        total, totalCompensation = kahanAdd(total, totalCompensation, inner)

    return (alternativesAbove + 1) * total / (n * n)


def agreementProbabilitySlow(n):
    alternativesAbove = n - 1
    total = Fraction(0, 1)

    for firstAbove in range(alternativesAbove + 1):
        for secondAbove in range(alternativesAbove - firstAbove + 1):
            firstAvoidance = Fraction(
                comb(alternativesAbove - firstAbove, secondAbove),
                comb(alternativesAbove, secondAbove),
            )
            for thirdAbove in range(
                alternativesAbove - firstAbove - secondAbove + 1
            ):
                secondAvoidance = Fraction(
                    comb(
                        alternativesAbove - firstAbove - secondAbove,
                        thirdAbove,
                    ),
                    comb(alternativesAbove, thirdAbove),
                )
                total += firstAvoidance * secondAvoidance

    return Fraction(total, n * n)


def solve():
    return f"{agreementProbability(TARGET_N):.10f}"


def runTests():
    assert agreementProbabilitySlow(3) == Fraction(17, 18)
    assert abs(agreementProbability(3) - 17 / 18) < 1e-15
    assert agreementProbabilitySlow(10) == Fraction(67079, 99225)
    assert abs(agreementProbability(10) - 0.6760292265) < 5e-11
    assert solve() == "0.0195868911"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
