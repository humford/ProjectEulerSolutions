import math
import time
from decimal import Decimal, ROUND_HALF_UP, getcontext


getcontext().prec = 80
EXACT_LIMIT = 200_000


def expectedQuestionsExact(n, p):
    if p <= 0.0 or p >= 1.0:
        return float(n)

    q = 1.0 - p
    logP = math.log(p)
    logQ = math.log(q)
    logGammaN = math.lgamma(n)
    shiftedTerms = []
    largestLog = -float("inf")

    for otherScore in range(n):
        logChoose = math.lgamma(n + otherScore) - logGammaN - math.lgamma(otherScore + 1)
        viewerWins = logChoose + otherScore * logP + n * logQ
        expertWins = logChoose + otherScore * logQ + n * logP
        shiftedTerms.append((n + otherScore, viewerWins, expertWins))
        largestLog = max(largestLog, viewerWins, expertWins)

    total = 0.0
    for questions, viewerWins, expertWins in shiftedTerms:
        total += questions * (
            math.exp(viewerWins - largestLog) + math.exp(expertWins - largestLog)
        )

    return math.exp(largestLog) * total


def normalGameProbabilityExact(n, p):
    return 1.0 - expectedQuestionsExact(n, p) / (2 * n + 1)


def underdogWinLogBound(n, p):
    lessLikely = min(p, Decimal(1) - p)
    trials = Decimal(2 * n - 1)
    excess = Decimal(n) - trials * lessLikely
    return -2 * excess * excess / trials


def normalGameProbabilityBiased(n, p):
    logBound = underdogWinLogBound(n, p)
    if logBound > Decimal("-30"):
        raise ValueError("bias is not strong enough for ten-decimal approximation")

    likelyProbability = max(p, Decimal(1) - p)
    return Decimal(1) - Decimal(n) / (likelyProbability * Decimal(2 * n + 1))


def normalGameProbability(n, p):
    if n <= EXACT_LIMIT:
        return normalGameProbabilityExact(n, float(p))
    return normalGameProbabilityBiased(n, Decimal(str(p)))


def roundedProbability(value):
    if isinstance(value, Decimal):
        return format(value.quantize(Decimal("0.0000000001"), rounding=ROUND_HALF_UP), "f")
    return format(value, ".10f")


def runTests():
    assert roundedProbability(normalGameProbability(6, Decimal("0.5"))) == "0.2851562500"
    assert roundedProbability(normalGameProbability(10, Decimal(3) / Decimal(7))) == "0.2330040743"
    assert roundedProbability(normalGameProbability(10_000, Decimal("0.3"))) == "0.2857499982"
    assert underdogWinLogBound(10 ** 11, Decimal("0.4999")) < Decimal("-4000")


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedProbability(normalGameProbability(10 ** 11, Decimal("0.4999")))
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
