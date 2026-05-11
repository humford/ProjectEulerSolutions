from collections import Counter
from math import factorial


def squareDigitSum(n):
    return sum(int(digit) ** 2 for digit in str(n))


def chainEnd(n, memo):
    sequence = []
    while n not in memo:
        sequence.append(n)
        n = squareDigitSum(n)

    end = memo[n]
    for value in sequence:
        memo[value] = end
    return end


def permutationCount(digits):
    count = factorial(len(digits))
    for repeated in Counter(digits).values():
        count //= factorial(repeated)
    return count


def countChainsEndingAt89BelowTenPower(digits):
    memo = {1: 1, 89: 89}
    count = 0

    def search(start_digit, remaining, chosen):
        nonlocal count
        if remaining == 0:
            if all(digit == 0 for digit in chosen):
                return
            total = sum(digit * digit for digit in chosen)
            if chainEnd(total, memo) == 89:
                count += permutationCount(chosen)
            return

        for digit in range(start_digit, 10):
            search(digit, remaining - 1, chosen + [digit])

    search(0, digits, [])
    return count


def runTests():
    memo = {1: 1, 89: 89}
    assert chainEnd(44, memo) == 1
    assert chainEnd(85, memo) == 89


def solve():
    return countChainsEndingAt89BelowTenPower(7)


if __name__ == "__main__":
    runTests()
    print(solve())
