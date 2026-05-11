def properDivisorSums(limit):
    sums = [0] * (limit + 1)
    for divisor in range(1, limit // 2 + 1):
        for multiple in range(divisor * 2, limit + 1, divisor):
            sums[multiple] += divisor
    return sums


def sumNonAbundantSums(limit):
    divisor_sums = properDivisorSums(limit)
    abundant = [value for value in range(1, limit + 1) if divisor_sums[value] > value]
    can_be_written = [False] * (limit + 1)

    for first_index, first in enumerate(abundant):
        for second in abundant[first_index:]:
            total = first + second
            if total > limit:
                break
            can_be_written[total] = True

    return sum(value for value in range(1, limit + 1) if not can_be_written[value])


def runTests():
    divisor_sums = properDivisorSums(28)
    assert divisor_sums[12] > 12
    assert divisor_sums[28] == 28
    assert sumNonAbundantSums(24) == 276


def solve():
    return sumNonAbundantSums(28123)


if __name__ == "__main__":
    runTests()
    print(solve())
