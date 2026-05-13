import math
import time


LAST_NINE_MODULUS = 10 ** 9


def fourthRootFloor(n):
    root = math.isqrt(math.isqrt(n))
    while (root + 1) ** 4 <= n:
        root += 1
    while root ** 4 > n:
        root -= 1
    return root


def upsideDownSolutionSum(limit, modulus=None):
    rLimit = fourthRootFloor((2 * limit * limit) // 13)
    mLimit = math.isqrt(rLimit)
    squares = [number * number for number in range(mLimit + 1)]

    total = 0
    reductionThreshold = 10 ** 20

    for m in range(1, mLimit + 1):
        mSquared = squares[m]
        nLimit = math.isqrt(rLimit - mSquared)
        nStart = 0 if m % 2 else 1

        for n in range(nStart, nLimit + 1, 2):
            if math.gcd(m, n) != 1:
                continue

            nSquared = squares[n]
            r = mSquared + nSquared
            realPart = mSquared - nSquared
            imaginaryPart = 2 * m * n

            a = abs(3 * realPart - 2 * imaginaryPart)
            b = abs(3 * imaginaryPart + 2 * realPart)
            p, q = (a, b) if a >= b else (b, a)

            if p % 13 == 0 and q % 13 == 0:
                continue

            x = q * r
            y = p * r
            if x > limit or y > limit:
                continue

            z = p * q
            if z > limit:
                continue

            total += x + y + z
            if modulus is not None and total >= reductionThreshold:
                total %= modulus

    return total if modulus is None else total % modulus


def runTests():
    assert upsideDownSolutionSum(10 ** 2) == 124
    assert upsideDownSolutionSum(10 ** 3) == 1_470
    assert upsideDownSolutionSum(10 ** 5) == 2_340_084


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = upsideDownSolutionSum(10 ** 16, LAST_NINE_MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer).zfill(9) + " in " + str(elapsed) + " seconds.")
