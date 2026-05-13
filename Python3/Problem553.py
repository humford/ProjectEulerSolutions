import time


MODULUS = 1_000_000_007


def factorialTables(limit):
    factorials = [1] * (limit + 1)
    inverseFactorials = [1] * (limit + 1)
    for number in range(1, limit + 1):
        factorials[number] = factorials[number - 1] * number % MODULUS

    inverseFactorials[limit] = pow(factorials[limit], MODULUS - 2, MODULUS)
    for number in range(limit, 0, -1):
        inverseFactorials[number - 1] = (
            inverseFactorials[number] * number
        ) % MODULUS

    return factorials, inverseFactorials


def modularInverses(limit):
    inverses = [0] * (limit + 1)
    inverses[1] = 1
    for number in range(2, limit + 1):
        inverses[number] = (
            MODULUS - (MODULUS // number) * inverses[MODULUS % number] % MODULUS
        )
    return inverses


def allCollectionsSeries(limit, inverseFactorials):
    coefficients = [0] * (limit + 1)
    for size in range(limit + 1):
        exponent = (pow(2, size, MODULUS - 1) - 1) % (MODULUS - 1)
        coefficients[size] = (
            pow(2, exponent, MODULUS) * inverseFactorials[size]
        ) % MODULUS
    return coefficients


def reciprocalSeries(series):
    limit = len(series) - 1
    reciprocal = [0] * (limit + 1)
    reciprocal[0] = pow(series[0], MODULUS - 2, MODULUS)

    for degree in range(1, limit + 1):
        total = 0
        for index in range(1, degree + 1):
            total += series[index] * reciprocal[degree - index]
        reciprocal[degree] = (-total) % MODULUS

    return reciprocal


def connectedSeries(limit, inverses, inverseFactorials):
    allCollections = allCollectionsSeries(limit, inverseFactorials)
    reciprocal = reciprocalSeries(allCollections)
    derivative = [
        (degree + 1) * allCollections[degree + 1] % MODULUS
        for degree in range(limit)
    ]

    logSeries = [0] * (limit + 1)
    for degree in range(limit):
        total = 0
        for index in range(degree + 1):
            total += derivative[index] * reciprocal[degree - index]
        logSeries[degree + 1] = total % MODULUS * inverses[degree + 1] % MODULUS

    # F(x) counts all collections.  F(x) = exp(x) * exp(A(x)), where exp(x)
    # accounts for unused labels, so connected component series A(x)=log(F)-x.
    logSeries[1] = (logSeries[1] - 1) % MODULUS
    return logSeries


def multiplySeries(left, right, limit):
    product = [0] * (limit + 1)
    for leftIndex, leftValue in enumerate(left):
        if leftValue == 0:
            continue
        for rightIndex in range(1, limit - leftIndex + 1):
            product[leftIndex + rightIndex] = (
                product[leftIndex + rightIndex]
                + leftValue * right[rightIndex]
            ) % MODULUS
    return product


def powerSetGraphCount(n, k):
    if k <= 0 or k > n:
        return 0

    factorials, inverseFactorials = factorialTables(n)
    inverses = modularInverses(n)
    connected = connectedSeries(n, inverses, inverseFactorials)

    componentPower = [0] * (n + 1)
    componentPower[0] = 1
    for _ in range(k):
        componentPower = multiplySeries(componentPower, connected, n)

    coefficient = 0
    for degree in range(n + 1):
        coefficient = (
            coefficient + componentPower[degree] * inverseFactorials[n - degree]
        ) % MODULUS

    return coefficient * factorials[n] % MODULUS * inverseFactorials[k] % MODULUS


def _components(vertices):
    remaining = set(range(len(vertices)))
    components = 0
    while remaining:
        components += 1
        stack = [remaining.pop()]
        while stack:
            index = stack.pop()
            connected = {
                other for other in remaining if vertices[index] & vertices[other]
            }
            remaining -= connected
            stack.extend(connected)
    return components


def brutePowerSetGraphCount(n, k):
    subsets = [mask for mask in range(1, 1 << n)]
    total = 0
    for chosenMask in range(1, 1 << len(subsets)):
        vertices = [
            subset for index, subset in enumerate(subsets) if chosenMask & (1 << index)
        ]
        if _components(vertices) == k:
            total += 1
    return total


def runTests():
    assert brutePowerSetGraphCount(2, 1) == 6
    assert brutePowerSetGraphCount(3, 1) == 111
    assert brutePowerSetGraphCount(4, 2) == 486
    assert powerSetGraphCount(2, 1) == 6
    assert powerSetGraphCount(3, 1) == 111
    assert powerSetGraphCount(4, 2) == 486
    assert powerSetGraphCount(100, 10) == 728_209_718


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = powerSetGraphCount(10 ** 4, 10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
