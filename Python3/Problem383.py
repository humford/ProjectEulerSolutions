import time


LIMIT = 10**18


def fiveExponent(number):
    total = 0

    while number % 5 == 0:
        number //= 5
        total += 1

    return total


def fiveExponentFactorial(number):
    total = 0

    while number > 0:
        number //= 5
        total += number

    return total


def baseFiveDigits(number):
    digits = []

    while number > 0:
        digits.append(number % 5)
        number //= 5

    return digits or [0]


def lowCarryCount(limit, maxCarries):
    digits = baseFiveDigits(limit)
    states = {(-1, 0, 0): 1}

    for position, limitDigit in enumerate(digits):
        nextStates = {}

        for (carry, borrow, carryCount), count in states.items():
            for digit in range(5):
                if position == 0 and digit == 0:
                    continue

                nextBorrow = 1 if digit + borrow > limitDigit else 0
                nextCarry = (2 * digit + carry) // 5
                nextCarryCount = carryCount + (1 if nextCarry > 0 else 0)

                if nextCarryCount > maxCarries:
                    continue

                key = (nextCarry, nextBorrow, nextCarryCount)
                nextStates[key] = nextStates.get(key, 0) + count

        states = nextStates

    return sum(
        count
        for (_carry, borrow, carryCount), count in states.items()
        if borrow == 0 and carryCount <= maxCarries
    )


def comparisonCount(limit=LIMIT):
    total = 0
    powerOfFive = 5
    exponent = 1

    while powerOfFive <= limit:
        total += lowCarryCount(limit // powerOfFive, exponent - 1)
        powerOfFive *= 5
        exponent += 1

    return total


def comparisonCountBrute(limit):
    return sum(
        1
        for index in range(1, limit + 1)
        if fiveExponentFactorial(2 * index - 1) < 2 * fiveExponentFactorial(index)
    )


def runTests():
    assert fiveExponent(625000) == 7
    assert comparisonCountBrute(10**3) == 68
    assert comparisonCount(10**3) == 68
    assert comparisonCount(10**9) == 2408210


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = comparisonCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
