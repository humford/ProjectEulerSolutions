import math
import time
from pathlib import Path


def readBaseExponents():
    path = Path(__file__).resolve().parents[1] / "Files" / "p099_base_exp.txt"
    return [
        tuple(int(value) for value in line.split(","))
        for line in path.read_text().strip().splitlines()
    ]


def compareExponential(base_exp):
    base, exponent = base_exp
    return exponent * math.log(base)


def largestExponentialLine(base_exponents):
    return max(
        range(1, len(base_exponents) + 1),
        key=lambda line: compareExponential(base_exponents[line - 1]),
    )


def runTests():
    assert largestExponentialLine([(2, 11), (3, 7)]) == 2


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestExponentialLine(readBaseExponents())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
