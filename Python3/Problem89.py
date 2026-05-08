import time
from pathlib import Path


ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

MINIMAL_PARTS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def readNumerals():
    path = Path(__file__).resolve().parents[1] / "Files" / "p089_roman.txt"
    return path.read_text().strip().splitlines()


def romanToInt(numeral):
    total = 0

    for index, char in enumerate(numeral):
        value = ROMAN_VALUES[char]
        if index + 1 < len(numeral) and ROMAN_VALUES[numeral[index + 1]] > value:
            total -= value
        else:
            total += value

    return total


def intToMinimalRoman(n):
    parts = []

    for value, numeral in MINIMAL_PARTS:
        count, n = divmod(n, value)
        parts.append(numeral * count)

    return "".join(parts)


def countSavedCharacters(numerals):
    return sum(len(numeral) - len(intToMinimalRoman(romanToInt(numeral))) for numeral in numerals)


def runTests():
    assert romanToInt("VIIII") == 9
    assert intToMinimalRoman(9) == "IX"
    assert intToMinimalRoman(49) == "XLIX"
    assert countSavedCharacters(["VIIII", "XXXXVIIII"]) == 8


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = countSavedCharacters(readNumerals())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
