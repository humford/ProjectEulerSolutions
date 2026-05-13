import time


STOP_PROBABILITY = 0.02
LETTER_PROBABILITY = 0.14
LETTERS = "IVXLCDM"

ONES = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
TENS = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
HUNDREDS = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]


def romanNumeralsBelowThousand():
    return [
        HUNDREDS[value // 100]
        + TENS[(value // 10) % 10]
        + ONES[value % 10]
        for value in range(1_000)
    ]


def suffixExpectations():
    romanByValue = romanNumeralsBelowThousand()
    valueByRoman = {
        roman: value
        for value, roman in enumerate(romanByValue)
    }

    successors = []
    for value, roman in enumerate(romanByValue):
        nextValues = []
        for letter in LETTERS:
            nextValue = valueByRoman.get(roman + letter)
            if nextValue is not None and nextValue > value:
                nextValues.append(nextValue)
        successors.append(nextValues)

    expectations = [0.0] * 1_000
    for value in range(999, 0, -1):
        nextValues = successors[value]
        if not nextValues:
            expectations[value] = value
        else:
            decisiveProbability = (
                STOP_PROBABILITY + LETTER_PROBABILITY * len(nextValues)
            )
            expectations[value] = (
                STOP_PROBABILITY * value
                + LETTER_PROBABILITY * sum(expectations[nextValue] for nextValue in nextValues)
            ) / decisiveProbability

    return expectations, valueByRoman


def romanNumeralExpectationValue():
    expectations, valueByRoman = suffixExpectations()
    firstSuffixExpectation = sum(
        expectations[valueByRoman[letter]]
        for letter in "IVXLCD"
    )
    return (
        LETTER_PROBABILITY
        / (1 - LETTER_PROBABILITY)
        * (1_000 + firstSuffixExpectation)
    )


def romanNumeralExpectation():
    return f"{romanNumeralExpectationValue():.8f}"


def runTests():
    expectations, valueByRoman = suffixExpectations()
    assert valueByRoman["XLIX"] == 49
    assert "IL" not in valueByRoman
    assert expectations[valueByRoman["IX"]] == 9
    assert romanNumeralExpectation() == "319.30207833"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = romanNumeralExpectation()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
