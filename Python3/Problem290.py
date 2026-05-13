import time
from collections import defaultdict


DIGITS = 18
MULTIPLIER = 137


def digitSum(number):
    total = 0

    while number:
        total += number % 10
        number //= 10

    return total


def digitalSignatureCount(digits):
    counts = {(0, 0): 1}

    for _ in range(digits):
        next_counts = defaultdict(int)

        for (carry, difference), count in counts.items():
            for digit in range(10):
                product = MULTIPLIER * digit + carry
                product_digit = product % 10
                next_carry = product // 10
                next_difference = difference + digit - product_digit

                next_counts[(next_carry, next_difference)] += count

        counts = next_counts

    return sum(
        count
        for (carry, difference), count in counts.items()
        if difference == digitSum(carry)
    )


def bruteDigitalSignatureCount(digits):
    return sum(
        1
        for number in range(10**digits)
        if digitSum(number) == digitSum(MULTIPLIER * number)
    )


def runTests():
    assert digitalSignatureCount(1) == bruteDigitalSignatureCount(1)
    assert digitalSignatureCount(2) == bruteDigitalSignatureCount(2)
    assert digitalSignatureCount(3) == bruteDigitalSignatureCount(3)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = digitalSignatureCount(DIGITS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
