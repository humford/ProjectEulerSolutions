ONES = {
    0: "",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
}

TENS = {
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
}


def numberToWords(n):
    if n == 1000:
        return "one thousand"
    if n >= 100:
        remainder = n % 100
        words = ONES[n // 100] + " hundred"
        if remainder:
            words += " and " + numberToWords(remainder)
        return words
    if n >= 20:
        remainder = n % 10
        words = TENS[n - remainder]
        if remainder:
            words += "-" + ONES[remainder]
        return words
    return ONES[n]


def numberLetterCount(n):
    return len(numberToWords(n).replace(" ", "").replace("-", ""))


def totalLetterCount(limit):
    return sum(numberLetterCount(n) for n in range(1, limit + 1))


def runTests():
    assert totalLetterCount(5) == 19
    assert numberLetterCount(342) == 23
    assert numberLetterCount(115) == 20


def solve():
    return totalLetterCount(1000)


if __name__ == "__main__":
    runTests()
    print(solve())
