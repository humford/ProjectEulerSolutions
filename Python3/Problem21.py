def properDivisorSum(n):
    if n <= 1:
        return 0

    total = 1
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            total += factor
            paired = n // factor
            if paired != factor:
                total += paired
        factor += 1

    return total


def sumAmicableNumbersUnder(limit):
    divisor_sums = {}
    total = 0

    for a in range(2, limit):
        b = divisor_sums.setdefault(a, properDivisorSum(a))
        if b != a and b > 0:
            divisor_sums.setdefault(b, properDivisorSum(b))
            if divisor_sums[b] == a:
                total += a

    return total


def runTests():
    assert properDivisorSum(220) == 284
    assert properDivisorSum(284) == 220


def solve():
    return sumAmicableNumbersUnder(10000)


if __name__ == "__main__":
    runTests()
    print(solve())
