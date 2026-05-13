import time
from math import isqrt


MOD = 433_494_437


def S(n, modulus=None):
    if n <= 0:
        return 0

    doubleN = 2 * n
    limit = isqrt(2 * n) + 2

    squarePrefix = [0] * (limit + 1)
    squarePrefixPrefix = [0] * (limit + 1)
    firstPowerPrefix = [0] * (limit + 1)
    secondPowerPrefix = [0] * (limit + 1)
    thirdPowerPrefix = [0] * (limit + 1)

    for i in range(1, limit + 1):
        square = i * i
        squarePrefix[i] = squarePrefix[i - 1] + square
        squarePrefixPrefix[i] = squarePrefixPrefix[i - 1] + squarePrefix[i]
        firstPowerPrefix[i] = firstPowerPrefix[i - 1] + i
        secondPowerPrefix[i] = secondPowerPrefix[i - 1] + square
        thirdPowerPrefix[i] = thirdPowerPrefix[i - 1] + square * i

    total = 0
    reduceLimit = 1 << 63

    def add(value):
        nonlocal total
        total += value
        if modulus is not None and total >= reduceLimit:
            total %= modulus

    # Edge cases with U < 2 are easiest to check directly.
    for U in range(2):
        for V in range(U + 1):
            for W in range(V + 1):
                for sign in (-1, 1):
                    if W == 0 and sign == -1:
                        continue
                    u = -U
                    v = -V
                    w = sign * W
                    m = U * U + V * V + W * W
                    if m == 0:
                        continue

                    a = (m + u + v + w) // 2
                    b = (m + u - v - w) // 2
                    c = (m - u + v - w) // 2
                    d = (m - u - v + w) // 2
                    if 1 <= a <= b <= c <= d <= n:
                        add(2 * m)

    for U in range(2, limit + 1):
        U2 = U * U
        remaining = doubleN - U2 - U
        if remaining < 0:
            break

        maxW0 = min(isqrt(remaining // 2), U)
        fullTest = doubleN - 2 * U2 - 2 * U

        for sign in (1, -1):
            startW = 0 if sign == 1 else 1
            if startW > maxW0:
                continue

            if fullTest < 0:
                fullW = -1
            else:
                root = isqrt(1 + 4 * fullTest)
                if sign == 1:
                    fullW = (root - 1) // 2
                else:
                    fullW = (root + 1) // 2
                fullW = min(fullW, maxW0)

            if fullW >= startW:
                A = startW
                B = fullW
                countW = B - A + 1

                sumW = firstPowerPrefix[B] - (firstPowerPrefix[A - 1] if A else 0)
                sumW2 = secondPowerPrefix[B] - (secondPowerPrefix[A - 1] if A else 0)
                sumW3 = thirdPowerPrefix[B] - (thirdPowerPrefix[A - 1] if A else 0)

                sumCount = countW * (U + 1) - sumW
                sumCountW2 = (U + 1) * sumW2 - sumW3

                if B == 0:
                    sumPrefix = 0
                else:
                    low = max(A - 1, 0)
                    high = B - 1
                    sumPrefix = squarePrefixPrefix[high] - (
                        squarePrefixPrefix[low - 1] if low > 0 else 0
                    )

                sumV2 = countW * squarePrefix[U] - sumPrefix
                add(2 * U2 * sumCount + 2 * sumCountW2 + 2 * sumV2)

            tailStart = max(fullW + 1, startW)
            if tailStart > maxW0:
                continue

            baseDiscriminant = 4 * doubleN + 1 - 4 * (U2 + U)
            for W in range(tailStart, maxW0 + 1):
                discriminant = baseDiscriminant - 4 * (W * W + sign * W)
                if discriminant < 0:
                    break

                maxV = min((isqrt(discriminant) - 1) // 2, U)
                if maxV < W:
                    continue

                count = maxV - W + 1
                sumV2 = squarePrefix[maxV] - (squarePrefix[W - 1] if W else 0)
                add(count * 2 * (U2 + W * W) + 2 * sumV2)

    return total if modulus is None else total % modulus


def runTests():
    assert S(5) == 48
    assert S(10 ** 3) == 37_048_340


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(10 ** 8, MOD)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
