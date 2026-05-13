import math
import time


EPSILON = 1e-14
MAX_ITERATIONS = 100_000
TAIL_PROBABILITY = 0.25


def gammaUpperTail(shape, x):
    # Continued fraction for Q(shape, x), the regularized upper incomplete gamma.
    tiny = 1e-300
    b = x + 1.0 - shape
    c = 1.0 / tiny
    d = 1.0 / b
    fraction = d

    for i in range(1, MAX_ITERATIONS + 1):
        an = -i * (i - shape)
        b += 2.0

        d = an * d + b
        if abs(d) < tiny:
            d = tiny

        c = b + an / c
        if abs(c) < tiny:
            c = tiny

        d = 1.0 / d
        delta = d * c
        fraction *= delta

        if abs(delta - 1.0) < EPSILON:
            front = math.exp(-x + shape * math.log(x) - math.lgamma(shape))
            return front * fraction

    raise RuntimeError("gamma continued fraction did not converge")


def inverseGammaUpperTail(shape, tailProbability):
    low = shape + 1.0
    high = shape + 10.0 * math.sqrt(shape)

    if gammaUpperTail(shape, low) <= tailProbability:
        raise ValueError("quantile is outside the continued-fraction bracket")

    while gammaUpperTail(shape, high) > tailProbability:
        high = shape + 2.0 * (high - shape)

    for _ in range(80):
        middle = (low + high) / 2.0
        if gammaUpperTail(shape, middle) > tailProbability:
            low = middle
        else:
            high = middle

    return (low + high) / 2.0


def criticalLog10Value(steps):
    logC = inverseGammaUpperTail(steps, TAIL_PROBABILITY)
    return "{:.2f}".format(logC / math.log(10.0))


def runTests():
    assert criticalLog10Value(100) == "46.27"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = criticalLog10Value(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
