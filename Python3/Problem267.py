import decimal
import math
import time


TOSSES = 1000
TARGET = 10**9


def minimumHeads(tosses, target):
    target_log = math.log(target)

    for heads in range(tosses + 1):
        if 3 * heads <= tosses:
            continue

        ratio = (3 * heads - tosses) / (2 * tosses)
        best_log = heads * math.log1p(2 * ratio) + (tosses - heads) * math.log1p(
            -ratio
        )

        if best_log >= target_log:
            return heads

    raise ValueError("target cannot be reached")


def binomialTail(tosses, heads):
    numerator = sum(math.comb(tosses, count) for count in range(heads, tosses + 1))
    denominator = 1 << tosses
    decimal.getcontext().prec = 80
    return decimal.Decimal(numerator) / decimal.Decimal(denominator)


def billionaireProbability(tosses, target):
    heads = minimumHeads(tosses, target)
    probability = binomialTail(tosses, heads)
    rounded = probability.quantize(
        decimal.Decimal("0.000000000001"), rounding=decimal.ROUND_HALF_UP
    )
    return format(rounded, ".12f")


def runTests():
    assert minimumHeads(TOSSES, TARGET) == 432


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = billionaireProbability(TOSSES, TARGET)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
