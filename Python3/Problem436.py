from decimal import Decimal, getcontext
import time


def sampleWinner():
    first = [0.62, 0.44]
    second = [0.10, 0.27, 0.91]
    x = first[-1]
    y = second[-1]

    return "second" if y > x else "first"


def secondPlayerWinProbability():
    getcontext().prec = 50
    e = Decimal(1).exp()
    probability = (14 * e - 5 * e * e + 1) / 4
    return format(probability, ".10f")


def runTests():
    assert sampleWinner() == "second"
    assert Decimal(secondPlayerWinProbability()) > Decimal("0.5")


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = secondPlayerWinProbability()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
