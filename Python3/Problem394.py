import math
import time


LIMIT = 40


def expectedRepeats(x=LIMIT):
    return (2 * math.log(x)) / 3 + 7 / 9 + 2 / (9 * x**3)


def answer():
    return format(expectedRepeats(), ".10f")


def runTests():
    assert format(expectedRepeats(1), ".10f") == "1.0000000000"
    assert format(expectedRepeats(2), ".10f") == "1.2676536759"
    assert format(expectedRepeats(7.5), ".10f") == "2.1215732071"


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = answer()
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")
