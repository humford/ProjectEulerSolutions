import time
from collections import deque


LIMIT = 10000


def restrictedDigitQuotient(divisor):
    parent = [-1] * divisor
    digit = [0] * divisor
    queue = deque()

    for first_digit in (1, 2):
        remainder = first_digit % divisor
        if parent[remainder] == -1:
            parent[remainder] = -2
            digit[remainder] = first_digit
            queue.append(remainder)

    while queue:
        remainder = queue.popleft()

        if remainder == 0:
            digits = []
            current = remainder

            while current != -2:
                digits.append(str(digit[current]))
                current = parent[current]

            return int("".join(reversed(digits))) // divisor

        for next_digit in (0, 1, 2):
            next_remainder = (10 * remainder + next_digit) % divisor

            if parent[next_remainder] == -1:
                parent[next_remainder] = remainder
                digit[next_remainder] = next_digit
                queue.append(next_remainder)

    raise RuntimeError("unreachable")


def restrictedDigitQuotientSum(limit):
    return sum(restrictedDigitQuotient(divisor) for divisor in range(1, limit + 1))


def runTests():
    assert restrictedDigitQuotient(2) == 1
    assert restrictedDigitQuotient(3) == 4
    assert restrictedDigitQuotient(7) == 3
    assert restrictedDigitQuotient(42) == 5
    assert restrictedDigitQuotient(89) == 12598
    assert restrictedDigitQuotientSum(100) == 11363107


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = restrictedDigitQuotientSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
