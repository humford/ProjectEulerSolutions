import functools
import fractions
import time


def roundFraction(value, digits):
    scale = 10 ** (digits + 1)
    quotient, _ = divmod(value.numerator * scale, value.denominator)
    lastDigit = quotient % 10
    quotient //= 10
    if lastDigit >= 5:
        quotient += 1

    integerPart = quotient // (10**digits)
    fractionalPart = quotient % (10**digits)
    return str(integerPart) + "." + format(fractionalPart, "0" + str(digits) + "d")


def evenPermutationProbability(n, length, spacing=40):
    target = fractions.Fraction(length, spacing) + 1

    @functools.lru_cache(None)
    def expectedSign(left, right, targetCoordinate):
        if left >= right:
            return fractions.Fraction(1, 1)

        count = right - left + 1
        indexSum = (left + right) * count // 2
        denominator = fractions.Fraction(count, 1) * targetCoordinate - indexSum

        total = fractions.Fraction(0, 1)
        for minimum in range(left, right + 1):
            probability = (targetCoordinate - minimum) / denominator
            sign = -1 if ((minimum - left) & 1) else 1
            lower = expectedSign(left, minimum - 1, fractions.Fraction(minimum, 1))
            upper = expectedSign(minimum + 1, right, targetCoordinate)
            total += probability * sign * lower * upper

        return total

    signExpectation = expectedSign(1, n, target)
    return (fractions.Fraction(1, 1) + signExpectation) / 2


def formattedEvenPermutationProbability(n, length):
    return roundFraction(evenPermutationProbability(n, length), 10)


def runTests():
    assert evenPermutationProbability(3, 160) == fractions.Fraction(56, 135)
    assert formattedEvenPermutationProbability(4, 400) == "0.5107843137"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedEvenPermutationProbability(13, 1_800)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
