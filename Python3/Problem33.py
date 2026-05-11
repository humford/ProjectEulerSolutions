from math import gcd


def cancelDigit(numerator, denominator, digit):
    numerator_text = str(numerator).replace(digit, "", 1)
    denominator_text = str(denominator).replace(digit, "", 1)
    if not numerator_text or not denominator_text:
        return None
    cancelled_denominator = int(denominator_text)
    if cancelled_denominator == 0:
        return None
    return int(numerator_text), cancelled_denominator


def digitCancellingFractions():
    fractions = []

    for numerator in range(10, 100):
        for denominator in range(numerator + 1, 100):
            if numerator % 10 == 0 and denominator % 10 == 0:
                continue
            for digit in set(str(numerator)) & set(str(denominator)) - {"0"}:
                cancelled = cancelDigit(numerator, denominator, digit)
                if cancelled is None:
                    continue
                reduced_numerator, reduced_denominator = cancelled
                if numerator * reduced_denominator == denominator * reduced_numerator:
                    fractions.append((numerator, denominator))

    return fractions


def productDenominator(fractions):
    numerator_product = 1
    denominator_product = 1

    for numerator, denominator in fractions:
        numerator_product *= numerator
        denominator_product *= denominator

    return denominator_product // gcd(numerator_product, denominator_product)


def runTests():
    assert (49, 98) in digitCancellingFractions()


def solve():
    return productDenominator(digitCancellingFractions())


if __name__ == "__main__":
    runTests()
    print(solve())
