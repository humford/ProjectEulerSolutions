import math
import time


MOD = 136_101_521


def lucasUPair(n, i, j):
    coefficient = 4 * n + 2
    maxIndex = max(i, j)

    if maxIndex == 0:
        return 0, 0
    if maxIndex == 1:
        return (1 if i == 1 else 0), (1 if j == 1 else 0)

    previous = 0
    current = 1
    ith = 1 if i == 1 else None
    jth = 1 if j == 1 else None

    for index in range(2, maxIndex + 1):
        previous, current = current, coefficient * current - previous
        if index == i:
            ith = current
        if index == j:
            jth = current

    return ith, jth


def cValue(n, i, j):
    triangle = n * (n + 1) // 2
    ui, uj = lucasUPair(n, i, j)
    return triangle * ui * uj


def maxNForPair(i, j, limit):
    high = 1
    while cValue(high, i, j) <= limit:
        high *= 2
    low = high // 2

    while low + 1 < high:
        mid = (low + high) // 2
        if cValue(mid, i, j) <= limit:
            low = mid
        else:
            high = mid

    return low


def forwardDifferences(values):
    coefficients = []
    current = list(values)

    while current:
        coefficients.append(current[0])
        current = [
            current[index + 1] - current[index]
            for index in range(len(current) - 1)
        ]

    return coefficients


def binomial(n, k):
    if k < 0 or k > n:
        return 0
    if k > n - k:
        k = n - k

    result = 1
    for value in range(1, k + 1):
        result = result * (n - k + value) // value

    return result


def polynomialPrefixSum(values, maxN):
    coefficients = forwardDifferences(values)
    total = 0

    for index, coefficient in enumerate(coefficients):
        total += coefficient * binomial(maxN + 1, index + 1)

    return total


def maxJForLimit(limit):
    previous = 0
    current = 1
    maxJ = 1

    for j in range(2, 400):
        previous, current = current, 6 * current - previous
        if current > limit:
            break
        maxJ = j

    return maxJ


def S(limit):
    maxJ = maxJForLimit(limit)
    total = 0

    for i in range(1, maxJ):
        for j in range(i + 1, maxJ + 1):
            if math.gcd(i, j) != 1:
                continue
            if cValue(1, i, j) > limit:
                continue

            maxN = maxNForPair(i, j, limit)
            if maxN <= 0:
                continue

            degree = i + j
            values = [cValue(n, i, j) for n in range(degree + 1)]
            total += polynomialPrefixSum(values, maxN)

    return total


def solve(limit):
    return S(limit) % MOD


def runTests():
    assert S(100) == 155
    assert S(10**5) == 1_479_802
    assert S(10**9) == 241_614_948_794


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve(10**35)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
