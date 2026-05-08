import time


def eCoefficient(index):
    if index == 0:
        return 2
    if index % 3 == 2:
        return 2 * ((index + 1) // 3)
    return 1


def convergentNumerator(term_count):
    numerator = 1
    denominator = 0

    for index in range(term_count - 1, -1, -1):
        numerator, denominator = (
            eCoefficient(index) * numerator + denominator,
            numerator,
        )

    return numerator


def digitSum(n):
    return sum(int(digit) for digit in str(n))


def runTests():
    assert [eCoefficient(index) for index in range(10)] == [2, 1, 2, 1, 1, 4, 1, 1, 6, 1]
    assert convergentNumerator(10) == 1457
    assert digitSum(1457) == 17


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = digitSum(convergentNumerator(100))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
