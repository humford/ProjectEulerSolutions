import fractions
import math
import time


def ramvok(values, cost):
    values = list(values)
    cost = fractions.Fraction(cost)
    expectedPrize = fractions.Fraction(0)
    bestProfit = fractions.Fraction(0)

    for turns in range(1, 500):
        previous = expectedPrize
        expectedPrize = sum(max(fractions.Fraction(value), expectedPrize) for value in values) / len(values)
        profit = expectedPrize - cost * turns
        bestProfit = max(bestProfit, profit)
        if turns > 10 and expectedPrize - previous < cost:
            break
    return bestProfit


def levelVisitWeights(dieSides):
    weights = []
    for target in range(1, dieSides + 1):
        lower = [0.0] * (dieSides + 1)
        diagonal = [0.0] * (dieSides + 1)
        upper = [0.0] * (dieSides + 1)
        rhs = [0.0] * (dieSides + 1)
        diagonal[0] = 1.0

        for visible in range(1, dieSides + 1):
            diagonal[visible] = 1.0
            rhs[visible] = 1.0 if visible == target else 0.0
            lower[visible] = -visible / dieSides
            if visible < dieSides:
                upper[visible] = -(dieSides - visible) / dieSides

        for row in range(1, dieSides + 1):
            factor = lower[row] / diagonal[row - 1]
            diagonal[row] -= factor * upper[row - 1]
            rhs[row] -= factor * rhs[row - 1]

        visits = [0.0] * (dieSides + 1)
        visits[dieSides] = rhs[dieSides] / diagonal[dieSides]
        for row in range(dieSides - 1, -1, -1):
            visits[row] = (rhs[row] - upper[row] * visits[row + 1]) / diagonal[row]

        weights.append(visits[dieSides] / math.comb(dieSides, target))
    return weights


def ramvokProfits(mask, dieSides, maxCost):
    maximumFace = mask.bit_length()
    values = [face + 1 for face in range(dieSides) if mask & (1 << face)]

    expectedPrize = 0.0
    previousPrize = 0.0
    prizes = []
    for turns in range(1, 200):
        total = 0.0
        for value in values:
            total += value if value > expectedPrize else expectedPrize
        previousPrize, expectedPrize = expectedPrize, total / len(values)
        prizes.append((turns, expectedPrize))
        if turns > 10 and expectedPrize - previousPrize < 1.0:
            break

    profits = [float(maximumFace)]
    for cost in range(1, maxCost + 1):
        profits.append(max(0.0, max(prize - cost * turns for turns, prize in prizes)))
    return profits


def superRamvokCosts(dieSides, maxCost):
    visitWeights = levelVisitWeights(dieSides)
    totalsByCostAndSize = [[0.0] * (dieSides + 1) for _ in range(maxCost + 1)]

    for mask in range(1, 1 << dieSides):
        visible = mask.bit_count()
        profits = ramvokProfits(mask, dieSides, maxCost)
        for cost, profit in enumerate(profits):
            totalsByCostAndSize[cost][visible] += profit

    totals = []
    for cost in range(maxCost + 1):
        total = 0.0
        for visible in range(1, dieSides + 1):
            total += visitWeights[visible - 1] * totalsByCostAndSize[cost][visible]
        totals.append(total)
    return totals


def superRamvok(dieSides, cost):
    return superRamvokCosts(dieSides, cost)[cost]


def superRamvokSum(n):
    total = 0.0
    for dieSides in range(4, n + 1):
        total += sum(superRamvokCosts(dieSides, n))
    return round(total)


def runTests():
    assert ramvok(range(1, 5), fractions.Fraction(1, 5)) == fractions.Fraction(53, 20)
    assert abs(superRamvok(6, 1) - 208.3) < 1e-9


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = superRamvokSum(20)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
