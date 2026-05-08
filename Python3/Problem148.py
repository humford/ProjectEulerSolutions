import time


def baseDigits(n, base):
    digits = []
    while n:
        digits.append(n % base)
        n //= base
    return list(reversed(digits)) or [0]


def nonDivisibleCount(row):
    product = 1
    for digit in baseDigits(row, 7):
        product *= digit + 1
    return product


def totalNonDivisibleRows(row_count):
    digits = baseDigits(row_count, 7)
    total = 0
    prefix_product = 1

    for index, digit in enumerate(digits):
        remaining = len(digits) - index - 1
        for smaller in range(digit):
            total += prefix_product * (smaller + 1) * (28 ** remaining)
        prefix_product *= digit + 1

    return total


def bruteTotal(row_count):
    return sum(nonDivisibleCount(row) for row in range(row_count))


def runTests():
    assert totalNonDivisibleRows(7) == 28
    assert totalNonDivisibleRows(100) == bruteTotal(100)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totalNonDivisibleRows(10 ** 9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
