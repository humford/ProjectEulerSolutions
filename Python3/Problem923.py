from collections import defaultdict
import time


MODULUS = 1_000_000_007
TARGET_M = 8
TARGET_W = 64


def ceilDivide(a, b):
    return (a + b - 1) // b


def reducedHook(a, b, k):
    # Repeatedly deleting the first row and first column of a Young diagram
    # preserves the one-square game value up to reversible moves.  For a
    # staircase, the remaining shape is the hook determined by the Durfee
    # square size d.
    durfee = 0

    for block in range(k):
        rowLength = (k - block) * b
        firstRow = block * a + 1
        if rowLength < firstRow:
            continue

        lastRow = (block + 1) * a
        durfee = max(durfee, min(lastRow, rowLength))

    rowBlock = (durfee - 1) // a
    rowLength = (k - rowBlock) * b
    armLength = rowLength - durfee + 1

    neededBlocks = ceilDivide(durfee, b)
    lastBlock = k - neededBlocks
    columnHeight = (lastBlock + 1) * a
    legLength = columnHeight - durfee + 1

    return armLength, legLength


def classifyStaircase(a, b, k):
    armLength, legLength = reducedHook(a, b, k)

    if legLength == 1:
        return "integer", armLength - 1
    if armLength == 1:
        return "integer", -(legLength - 1)

    leftOption = armLength - 2
    rightOption = -(legLength - 2)
    temperature = leftOption - rightOption

    return "hot", (temperature, rightOption)


def staircaseValueCounts(w):
    integerCounts = defaultdict(int)
    hotCounts = defaultdict(int)

    for a in range(1, w - 1):
        for b in range(1, w - a):
            for k in range(1, w - a - b + 1):
                valueType, value = classifyStaircase(a, b, k)
                if valueType == "integer":
                    integerCounts[value] += 1
                else:
                    hotCounts[value] += 1

    return integerCounts, hotCounts


def factorials(n):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MODULUS

    inverseFact = [1] * (n + 1)
    inverseFact[n] = pow(fact[n], MODULUS - 2, MODULUS)
    for i in range(n, 0, -1):
        inverseFact[i - 1] = inverseFact[i] * i % MODULUS

    return fact, inverseFact


def typeMultiplicityPolynomial(count, maxDegree, inverseFact):
    coefficients = [1] + [0] * maxDegree
    power = 1

    for degree in range(1, maxDegree + 1):
        power = power * count % MODULUS
        coefficients[degree] = power * inverseFact[degree] % MODULUS

    return coefficients


def hotComponentDp(hotCounts, m, inverseFact):
    dp = [[defaultdict(int) for _ in range(2)] for _ in range(m + 1)]
    dp[0][0][0] = 1

    hotTypes = sorted(
        ((temperature, rightOption, count) for (temperature, rightOption), count in hotCounts.items()),
        key=lambda item: (-item[0], item[1]),
    )

    for temperature, rightOption, count in hotTypes:
        polynomial = typeMultiplicityPolynomial(count, m, inverseFact)
        nextDp = [[defaultdict(int) for _ in range(2)] for _ in range(m + 1)]

        for used in range(m + 1):
            for parity in (0, 1):
                for total, coefficient in dp[used][parity].items():
                    for copies in range(m - used + 1):
                        multiplier = polynomial[copies]
                        if multiplier == 0:
                            continue

                        rightTurns = (copies + 1 - parity) // 2
                        delta = copies * rightOption + rightTurns * temperature
                        nextUsed = used + copies
                        nextParity = parity ^ (copies & 1)
                        nextTotal = total + delta
                        nextDp[nextUsed][nextParity][nextTotal] = (
                            nextDp[nextUsed][nextParity][nextTotal]
                            + coefficient * multiplier
                        ) % MODULUS

        dp = nextDp

    return dp


def integerComponentDp(integerCounts, m, inverseFact):
    dp = [defaultdict(int) for _ in range(m + 1)]
    dp[0][0] = 1

    for value, count in integerCounts.items():
        polynomial = typeMultiplicityPolynomial(count, m, inverseFact)
        nextDp = [defaultdict(int) for _ in range(m + 1)]

        for used in range(m + 1):
            for total, coefficient in dp[used].items():
                for copies in range(m - used + 1):
                    multiplier = polynomial[copies]
                    if multiplier == 0:
                        continue

                    nextDp[used + copies][total + copies * value] = (
                        nextDp[used + copies][total + copies * value]
                        + coefficient * multiplier
                    ) % MODULUS

        dp = nextDp

    return dp


def S(m, w):
    fact, inverseFact = factorials(m)
    integerCounts, hotCounts = staircaseValueCounts(w)
    hotDp = hotComponentDp(hotCounts, m, inverseFact)
    integerDp = integerComponentDp(integerCounts, m, inverseFact)

    multisetCount = 0
    for hotUsed in range(m + 1):
        for parity in (0, 1):
            for hotTotal, hotCoefficient in hotDp[hotUsed][parity].items():
                for integerTotal, integerCoefficient in integerDp[m - hotUsed].items():
                    total = hotTotal + integerTotal
                    if total > 0 or (total == 0 and parity == 1):
                        multisetCount = (
                            multisetCount + hotCoefficient * integerCoefficient
                        ) % MODULUS

    return multisetCount * fact[m] % MODULUS


def solve():
    return S(TARGET_M, TARGET_W)


def runTests():
    assert reducedHook(1, 1, 2) == (2, 2)
    assert classifyStaircase(1, 1, 2) == ("hot", (0, 0))
    assert S(2, 4) == 7
    assert S(3, 9) == 315_319
    assert solve() == 740_759_929


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
