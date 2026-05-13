import time
from fractions import Fraction


DICE = (4, 6, 8, 12, 20)


def dieMean(sides):
    return Fraction(sides + 1, 2)


def dieVariance(sides):
    return Fraction(sides * sides - 1, 12)


def platonicDiceVariance():
    mean = dieMean(DICE[0])
    variance = dieVariance(DICE[0])

    for sides in DICE[1:]:
        mean, variance = (
            mean * dieMean(sides),
            mean * dieVariance(sides) + variance * dieMean(sides) ** 2,
        )

    return variance


def answer():
    return format(float(platonicDiceVariance()), ".4f")


def runTests():
    assert dieMean(6) == Fraction(7, 2)
    assert dieVariance(6) == Fraction(35, 12)
    assert platonicDiceVariance() == Fraction(2464129395, 1024)


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = answer()
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")
