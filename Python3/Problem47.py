def distinctPrimeFactorCounts(limit):
    counts = [0] * (limit + 1)
    for factor in range(2, limit + 1):
        if counts[factor] == 0:
            for multiple in range(factor, limit + 1, factor):
                counts[multiple] += 1
    return counts


def firstConsecutiveWithPrimeFactors(consecutive, distinctFactors, limit):
    counts = distinctPrimeFactorCounts(limit)
    run_length = 0

    for value in range(2, limit + 1):
        if counts[value] == distinctFactors:
            run_length += 1
            if run_length == consecutive:
                return value - consecutive + 1
        else:
            run_length = 0

    raise ValueError("No sequence found below %s" % limit)


def runTests():
    assert firstConsecutiveWithPrimeFactors(2, 2, 100) == 14
    assert firstConsecutiveWithPrimeFactors(3, 3, 1000) == 644


def solve():
    return firstConsecutiveWithPrimeFactors(4, 4, 200000)


if __name__ == "__main__":
    runTests()
    print(solve())
