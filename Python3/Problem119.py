import time


def digitSum(n):
    return sum(int(digit) for digit in str(n))


def digitPowerValues(count):
    values = set()
    max_digits = 2

    while len(values) < count:
        limit = 10 ** max_digits
        max_base = 9 * max_digits

        for base in range(2, max_base + 1):
            value = base * base
            while value < limit:
                if value >= 10 and digitSum(value) == base:
                    values.add(value)
                value *= base

        max_digits += 1

    return sorted(values)


def nthDigitPowerValue(index):
    return digitPowerValues(index)[index - 1]


def runTests():
    assert digitPowerValues(2)[:2] == [81, 512]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nthDigitPowerValue(30)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
