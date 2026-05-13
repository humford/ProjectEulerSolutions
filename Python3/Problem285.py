import math
import time


LIMIT = 10**5


def shiftedQuarterCircleArea(radius):
    if radius <= math.sqrt(2):
        return 0.0

    upper = math.sqrt(radius * radius - 1)

    def antiderivative(x):
        return (
            0.5
            * (
                x * math.sqrt(max(0.0, radius * radius - x * x))
                + radius * radius * math.asin(x / radius)
            )
            - x
        )

    return antiderivative(upper) - antiderivative(1)


def expectedScore(limit):
    total = 0.0

    for k in range(1, limit + 1):
        area = shiftedQuarterCircleArea(k + 0.5) - shiftedQuarterCircleArea(k - 0.5)
        total += area / k

    return total


def runTests():
    assert format(expectedScore(10), ".5f") == "10.20914"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = format(expectedScore(LIMIT), ".5f")
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
