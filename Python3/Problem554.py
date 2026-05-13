import math
import time


MODULUS = 100_000_007
HALF_MODULUS = (MODULUS - 1) // 2
STATES = ((0, 0), (0, 1), (1, 0), (1, 1))


def centaurAttacks(first, second):
    rowDistance = abs(first[0] - second[0])
    columnDistance = abs(first[1] - second[1])
    return (
        max(rowDistance, columnDistance) == 1
        and rowDistance + columnDistance > 0
    ) or sorted((rowDistance, columnDistance)) == [1, 2]


def boardPosition(blockRow, blockColumn, state):
    rowOffset, columnOffset = state
    return 2 * blockRow + rowOffset, 2 * blockColumn + columnOffset


def rowPatterns(n):
    patterns = []

    def extend(pattern):
        if len(pattern) == n:
            patterns.append(tuple(pattern))
            return

        column = len(pattern)
        for state in STATES:
            if pattern and centaurAttacks(
                boardPosition(0, column - 1, pattern[-1]),
                boardPosition(0, column, state),
            ):
                continue
            extend(pattern + [state])

    extend([])
    return patterns


def rowsCompatible(upper, lower):
    n = len(upper)
    for column in range(n):
        if centaurAttacks(
            boardPosition(0, column, upper[column]),
            boardPosition(1, column, lower[column]),
        ):
            return False

    for column in range(n - 1):
        if centaurAttacks(
            boardPosition(0, column, upper[column]),
            boardPosition(1, column + 1, lower[column + 1]),
        ):
            return False
        if centaurAttacks(
            boardPosition(0, column + 1, upper[column + 1]),
            boardPosition(1, column, lower[column]),
        ):
            return False

    return True


def transferCentaurPlacements(n):
    patterns = rowPatterns(n)
    compatible = [
        [
            lowerIndex
            for lowerIndex, lower in enumerate(patterns)
            if rowsCompatible(upper, lower)
        ]
        for upper in patterns
    ]

    counts = [1] * len(patterns)
    for _ in range(n - 1):
        nextCounts = [0] * len(patterns)
        for upperIndex, count in enumerate(counts):
            if count == 0:
                continue
            for lowerIndex in compatible[upperIndex]:
                nextCounts[lowerIndex] += count
        counts = nextCounts

    return sum(counts)


def centaurPlacements(n):
    return 8 * math.comb(2 * n, n) - 3 * n * n - 2 * n - 7


def fibonacciNumbers(lastIndex):
    values = [0, 1]
    for _ in range(2, lastIndex + 1):
        values.append(values[-1] + values[-2])
    return values


def carryFreeDigits(number):
    digits = []
    while number:
        digit = number % MODULUS
        if digit > HALF_MODULUS:
            return None
        digits.append(digit)
        number //= MODULUS
    return digits or [0]


def centralBinomialTargets(values):
    targets = {0}
    for value in values:
        digits = carryFreeDigits(value)
        if digits is None:
            continue
        for digit in digits:
            targets.add(digit)
            targets.add(2 * digit)
    return targets


def factorialValues(targets):
    values = {0: 1}
    factorial = 1
    previous = 0
    for target in sorted(targets):
        for number in range(previous + 1, target + 1):
            factorial = factorial * number % MODULUS
        values[target] = factorial
        previous = target
    return values


def smallCentralBinomial(digit, factorials):
    denominator = factorials[digit] * factorials[digit] % MODULUS
    return factorials[2 * digit] * pow(denominator, MODULUS - 2, MODULUS) % MODULUS


def centralBinomialModulo(n, factorials):
    digits = carryFreeDigits(n)
    if digits is None:
        return 0

    result = 1
    for digit in digits:
        result = result * smallCentralBinomial(digit, factorials) % MODULUS
    return result


def centaurPlacementsModulo(n, factorials):
    reduced = n % MODULUS
    central = centralBinomialModulo(n, factorials)
    return (8 * central - 3 * reduced * reduced - 2 * reduced - 7) % MODULUS


def fibonacciCentaurSum(lastIndex=90):
    fibonacci = fibonacciNumbers(lastIndex)
    arguments = fibonacci[2 : lastIndex + 1]
    factorials = factorialValues(centralBinomialTargets(arguments))
    return sum(centaurPlacementsModulo(n, factorials) for n in arguments) % MODULUS


def runTests():
    assert centaurPlacements(1) == 4
    assert centaurPlacements(2) == 25
    assert centaurPlacements(10) == 1_477_721
    for n in range(1, 8):
        assert transferCentaurPlacements(n) == centaurPlacements(n)

    factorials = factorialValues(centralBinomialTargets([10]))
    assert centaurPlacementsModulo(10, factorials) == 1_477_721


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciCentaurSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
