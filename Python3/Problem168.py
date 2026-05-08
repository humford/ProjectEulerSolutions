import time


def rotatingNumbers(max_digits):
    values = []

    for digits in range(2, max_digits + 1):
        power = 10 ** (digits - 1)

        for multiplier in range(1, 10):
            denominator = 10 * multiplier - 1
            for last_digit in range(1, 10):
                numerator = last_digit * (power - multiplier)
                if numerator % denominator != 0:
                    continue

                prefix = numerator // denominator
                if power // 10 <= prefix < power:
                    values.append(10 * prefix + last_digit)

    return values


def lastFiveDigitsOfSum(max_digits):
    return sum(rotatingNumbers(max_digits)) % 100000


def runTests():
    assert 142857 in rotatingNumbers(6)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lastFiveDigitsOfSum(100)
    elapsed = time.time() - start

    print("Found " + str(answer).zfill(5) + " in " + str(elapsed) + " seconds.")
