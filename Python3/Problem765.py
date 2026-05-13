import time


def binomialCoefficients(n):
    values = [1] * (n + 1)
    for k in range(1, n + 1):
        values[k] = values[k - 1] * (n - k + 1) // k
    return values


def roundHalfUpDecimal(numerator, denominator, digits):
    scale = 10 ** digits
    quotient, remainder = divmod(numerator * scale, denominator)
    if 2 * remainder >= denominator:
        quotient += 1
    integerPart, fractionalPart = divmod(quotient, scale)
    return str(integerPart) + "." + str(fractionalPart).zfill(digits)


def optimalSuccessProbability(n, target, winNumerator=3, probabilityDenominator=5):
    totalPaths = 1 << n
    pathBudget = totalPaths // target
    denominator = probabilityDenominator ** n
    if pathBudget <= 0:
        return 0, denominator
    if pathBudget >= totalPaths:
        return denominator, denominator

    combinations = binomialCoefficients(n)
    suffixCounts = [0] * (n + 2)
    for wins in range(n, -1, -1):
        suffixCounts[wins] = suffixCounts[wins + 1] + combinations[wins]

    threshold = None
    for wins in range(n, -1, -1):
        if suffixCounts[wins] > pathBudget >= suffixCounts[wins + 1]:
            threshold = wins
            break
    assert threshold is not None

    takenAtThreshold = pathBudget - suffixCounts[threshold + 1]
    lossNumerator = probabilityDenominator - winNumerator

    winPowers = [1] * (n + 1)
    lossPowers = [1] * (n + 1)
    for exponent in range(1, n + 1):
        winPowers[exponent] = winPowers[exponent - 1] * winNumerator
        lossPowers[exponent] = lossPowers[exponent - 1] * lossNumerator

    numerator = 0
    for wins in range(threshold + 1, n + 1):
        numerator += combinations[wins] * winPowers[wins] * lossPowers[n - wins]
    numerator += takenAtThreshold * winPowers[threshold] * lossPowers[n - threshold]

    return numerator, denominator


def solve():
    numerator, denominator = optimalSuccessProbability(1000, 10 ** 12)
    return roundHalfUpDecimal(numerator, denominator, 10)


def runTests():
    assert roundHalfUpDecimal(1, 3, 10) == "0.3333333333"
    assert roundHalfUpDecimal(2, 3, 10) == "0.6666666667"

    assert optimalSuccessProbability(5, 1) == (5 ** 5, 5 ** 5)
    assert optimalSuccessProbability(5, 33) == (0, 5 ** 5)

    numerator, denominator = optimalSuccessProbability(5, 32)
    assert numerator == 3 ** 5
    assert denominator == 5 ** 5

    numerator, denominator = optimalSuccessProbability(3, 2)
    assert numerator == 3 ** 3 + 3 * 3 ** 2 * 2
    assert denominator == 5 ** 3


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
