import math
import time


def expectedColours():
    missing_one_colour = math.comb(60, 20) / math.comb(70, 20)
    return "{:.9f}".format(7 * (1 - missing_one_colour))


def runTests():
    assert expectedColours() == "6.818741802"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedColours()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
