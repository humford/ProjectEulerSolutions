import math
import time


ROOT_CACHE = {}


def expectedGainRoot(cost):
    if cost in ROOT_CACHE:
        return ROOT_CACHE[cost]

    upper = -1e-12
    while rootFunction(upper, cost) <= 0:
        upper *= 0.5

    lower = upper
    while rootFunction(lower, cost) > 0:
        lower *= 2
        if lower < -100:
            raise RuntimeError("Could not bracket negative root")

    for _ in range(120):
        middle = (lower + upper) / 2
        if rootFunction(middle, cost) > 0:
            upper = middle
        else:
            lower = middle

    root = (lower + upper) / 2
    ROOT_CACHE[cost] = root
    return root


def rootFunction(value, cost):
    total = 0.0
    compensation = 0.0
    multiplier = 1.0
    probability = 0.5

    for _ in range(200):
        term = probability * math.expm1(multiplier * value)
        adjusted = term - compensation
        nextTotal = total + adjusted
        compensation = (nextTotal - total) - adjusted
        total = nextTotal

        if probability < 2 ** -90:
            break

        multiplier *= 2
        probability *= 0.5

    return math.expm1(cost * value) - total


def survivalProbability(cost, fortune):
    if fortune < cost:
        return 0.0

    root = expectedGainRoot(cost)
    return -math.expm1(root * (fortune - cost + 1))


def roundedSurvivalProbability(cost, fortune, digits):
    return f"{survivalProbability(cost, fortune):.{digits}f}"


def runTests():
    assert survivalProbability(2, 1) == 0.0
    assert roundedSurvivalProbability(2, 2, 4) == "0.2522"
    assert roundedSurvivalProbability(2, 5, 4) == "0.6873"
    assert roundedSurvivalProbability(6, 10_000, 4) == "0.9952"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedSurvivalProbability(15, 10 ** 9, 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
