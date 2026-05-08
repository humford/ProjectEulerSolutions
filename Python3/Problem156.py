import time


def countDigit(n, digit):
    count = 0
    factor = 1

    while factor <= n:
        lower = n % factor
        current = (n // factor) % 10
        higher = n // (factor * 10)

        if current > digit:
            count += (higher + 1) * factor
        elif current == digit:
            count += higher * factor + lower + 1
        else:
            count += higher * factor

        factor *= 10

    return count


def fixedPointsForDigit(digit, upper_bound):
    fixed_points = []
    stack = [(1, upper_bound)]

    while stack:
        low, high = stack.pop()
        low_count = countDigit(low, digit)
        high_count = countDigit(high, digit)

        if low_count > high or high_count < low:
            continue

        if high - low < 1000:
            for n in range(low, high + 1):
                if countDigit(n, digit) == n:
                    fixed_points.append(n)
            continue

        middle = (low + high) // 2
        stack.append((middle + 1, high))
        stack.append((low, middle))

    return fixed_points


def fixedPointSum(upper_bound):
    return sum(
        sum(fixedPointsForDigit(digit, upper_bound))
        for digit in range(1, 10)
    )


def runTests():
    assert countDigit(13, 1) == 6
    assert fixedPointsForDigit(1, 10) == [1]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fixedPointSum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
