def reverseNumber(n):
    return int(str(n)[::-1])


def isReversible(n):
    if n % 10 == 0:
        return False
    return all(int(digit) % 2 == 1 for digit in str(n + reverseNumber(n)))


def bruteReversibleCount(limit):
    return sum(1 for n in range(1, limit) if isReversible(n))


def reversibleCountBelowPowerOfTen(digits):
    count = 0

    for digit_count in range(1, digits + 1):
        if digit_count % 2 == 0:
            count += 20 * (30 ** (digit_count // 2 - 1))
        elif digit_count % 4 == 3:
            count += 100 * (500 ** (digit_count // 4))

    return count


def runTests():
    assert isReversible(36)
    assert not isReversible(10)
    assert bruteReversibleCount(1000) == 120
    assert reversibleCountBelowPowerOfTen(3) == 120


def solve():
    return reversibleCountBelowPowerOfTen(9)


if __name__ == "__main__":
    runTests()
    print(solve())
