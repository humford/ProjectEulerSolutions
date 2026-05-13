from math import isqrt
import time


TARGET_N = 1_000_000
DIGIT_COSTS = (6, 2, 5, 5, 4, 5, 6, 3, 7, 6)
OPERATOR_COST = 2


def digitCostsUpTo(limit):
    costs = bytearray(limit + 1)

    for number in range(1, limit + 1):
        costs[number] = costs[number // 10] + DIGIT_COSTS[number % 10]

    return costs


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))

    for value in range(2, isqrt(limit) + 1):
        if factors[value] != value:
            continue
        for multiple in range(value * value, limit + 1, value):
            if factors[multiple] == multiple:
                factors[multiple] = value

    return factors


def divisorsFromFactorization(number, smallestFactor):
    factors = []

    while number > 1:
        prime = smallestFactor[number]
        exponent = 0
        while number % prime == 0:
            number //= prime
            exponent += 1
        factors.append((prime, exponent))

    divisors = [1]
    for prime, exponent in factors:
        previous = divisors
        divisors = []
        primePower = 1
        for _ in range(exponent + 1):
            for divisor in previous:
                divisors.append(divisor * primePower)
            primePower *= prime

    return divisors


def productCosts(limit):
    digitCosts = digitCostsUpTo(limit)
    smallestFactor = smallestPrimeFactors(limit)
    costs = bytearray(digitCosts)
    costs[0] = 255

    for number in range(2, limit + 1):
        if smallestFactor[number] == number:
            continue

        best = costs[number]
        root = isqrt(number)
        for divisor in divisorsFromFactorization(number, smallestFactor):
            if 1 < divisor <= root:
                candidate = costs[divisor] + costs[number // divisor] + OPERATOR_COST
                if candidate < best:
                    best = candidate
        costs[number] = best

    return costs


def updatePairsSameCost(values, candidateCost, output):
    limit = len(output) - 1
    valueCount = len(values)

    for i, a in enumerate(values):
        maxB = limit - a
        j = valueCount - 1
        while j >= i and values[j] > maxB:
            j -= 1
        for k in range(i, j + 1):
            total = a + values[k]
            if candidateCost < output[total]:
                output[total] = candidateCost


def updatePairsDifferentCost(leftValues, rightValues, candidateCost, output):
    limit = len(output) - 1

    if len(leftValues) > len(rightValues):
        leftValues, rightValues = rightValues, leftValues

    maxIndex = len(rightValues) - 1
    for left in leftValues:
        maxRight = limit - left
        while maxIndex >= 0 and rightValues[maxIndex] > maxRight:
            maxIndex -= 1
        for index in range(maxIndex + 1):
            total = left + rightValues[index]
            if candidateCost < output[total]:
                output[total] = candidateCost


def bucketByCost(costs, maxCost):
    buckets = [[] for _ in range(maxCost + 1)]

    for value in range(1, len(costs)):
        cost = costs[value]
        if cost <= maxCost:
            buckets[cost].append(value)

    return buckets


def twoTermCosts(limit, products):
    costs = bytearray(products)
    buckets = bucketByCost(products, 40)

    for firstCost in range(2, 33):
        left = buckets[firstCost]
        if not left:
            continue
        for secondCost in range(firstCost, 33 - firstCost):
            right = buckets[secondCost]
            if not right:
                continue

            candidate = firstCost + secondCost + OPERATOR_COST
            if firstCost == secondCost:
                updatePairsSameCost(left, candidate, costs)
            else:
                updatePairsDifferentCost(left, right, candidate, costs)

    cheapSummands = []
    for cost in range(2, 19):
        cheapSummands.extend(buckets[cost])
    cheapSummands.sort()

    for number in range(1, limit + 1):
        if costs[number] <= 34:
            continue

        best = costs[number]
        half = number // 2
        for left in cheapSummands:
            if left > half:
                break
            candidate = products[left] + products[number - left] + OPERATOR_COST
            if candidate < best:
                best = candidate
        costs[number] = best

    return costs


def bestTwoProductSum(limit, products, costLimit):
    buckets = bucketByCost(products, costLimit)
    best = bytearray([255]) * (limit + 1)

    for firstCost in range(2, costLimit + 1):
        left = buckets[firstCost]
        if not left:
            continue
        for secondCost in range(firstCost, costLimit - firstCost + 1):
            right = buckets[secondCost]
            if not right:
                continue

            candidate = firstCost + secondCost
            if firstCost == secondCost:
                updatePairsSameCost(left, candidate, best)
            else:
                updatePairsDifferentCost(left, right, candidate, best)

    return best


def applyThreeTermFix(limit, products, costs):
    bestPair = bestTwoProductSum(limit, products, 30)

    cheapThirdTerms = [
        value
        for value in range(1, limit + 1)
        if products[value] <= 20
    ]
    smallRemainders = [
        value
        for value in range(2, limit + 1)
        if bestPair[value] != 255 and bestPair[value] <= 8
    ]

    for number in range(1, limit + 1):
        current = costs[number]
        if current < 33:
            continue

        pairLimit = current - 5
        if pairLimit < 6:
            continue

        best = current
        for third in cheapThirdTerms:
            if third >= number:
                break
            thirdCost = products[third]
            if thirdCost > pairLimit:
                continue
            remainder = number - third
            pairCost = bestPair[remainder]
            if pairCost != 255 and pairCost + thirdCost <= pairLimit:
                best = pairCost + thirdCost + 2 * OPERATOR_COST
                if best == current - 1:
                    break

        if best > current - 1:
            for remainder in smallRemainders:
                if remainder >= number:
                    break
                pairCost = bestPair[remainder]
                third = number - remainder
                if pairCost + products[third] <= pairLimit:
                    best = pairCost + products[third] + 2 * OPERATOR_COST
                    if best == current - 1:
                        break

        costs[number] = best


def exactSmallCosts(limit):
    products = productCosts(limit)
    costs = bytearray([255]) * (limit + 1)
    costs[0] = 0

    for value in range(1, limit + 1):
        termCost = products[value] + OPERATOR_COST
        for total in range(value, limit + 1):
            candidate = costs[total - value] + termCost
            if candidate < costs[total]:
                costs[total] = candidate

    for value in range(1, limit + 1):
        costs[value] -= OPERATOR_COST

    return costs


def minimumCosts(limit):
    products = productCosts(limit)
    costs = twoTermCosts(limit, products)
    applyThreeTermFix(limit, products, costs)
    return costs


def solve():
    costs = minimumCosts(TARGET_N)
    return sum(costs[1:])


def runTests():
    small = minimumCosts(100)
    assert small[1:] == exactSmallCosts(100)[1:]
    assert small[28] == 9
    assert sum(small[1:]) == 916


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    assert answer == 26688208
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
