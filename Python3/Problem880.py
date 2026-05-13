from math import gcd, isqrt
import time


TARGET_N = 10**15
MODULUS = 1031**3 + 2


def integerCubeRoot(n):
    root = int(round(n ** (1.0 / 3.0)))

    while (root + 1) ** 3 <= n:
        root += 1
    while root**3 > n:
        root -= 1

    return root


def isPerfectCube(n):
    return integerCubeRoot(n) ** 3 == n


def isRationalCubeRatio(x, y):
    divisor = gcd(abs(x), abs(y))
    return (
        isPerfectCube(abs(x) // divisor)
        and isPerfectCube(abs(y) // divisor)
    )


def squareSum(limit):
    return limit * (limit + 1) * (2 * limit + 1) // 6


def primitivePair(p, q):
    parityDivisor = gcd(p, 2)
    denominator = parityDivisor * parityDivisor

    x = p * (p + 4 * q) ** 3 // denominator
    y = -4 * q * (2 * p - q) ** 3 // denominator

    if abs(x) <= abs(y):
        return x, y
    return y, x


def maxQForP(limit, p):
    parityDivisor = gcd(p, 2)
    maximumSum = integerCubeRoot(limit * parityDivisor * parityDivisor // p)
    return (maximumSum - p) // 4


def H(limit, modulus=None):
    total = 0
    p = 1

    while p * (p + 4) ** 3 <= 4 * limit:
        for q in range(1, maxQForP(limit, p) + 1):
            if gcd(p, q) != 1:
                continue

            x, y = primitivePair(p, q)
            if x == 0 or y == 0:
                continue

            largest = max(abs(x), abs(y))
            if largest > limit or isRationalCubeRatio(x, y):
                continue

            maximumScale = isqrt(limit // largest)
            contribution = (abs(x) + abs(y)) * squareSum(maximumScale)

            if modulus is None:
                total += contribution
            else:
                total = (total + contribution) % modulus

        p += 1

    return total


def solve():
    return H(TARGET_N, MODULUS)


def runTests():
    assert primitivePair(1, 1) == (-4, 125)
    assert primitivePair(2, 5) == (5, 5324)
    assert H(10**3) == 2535
    assert H(10**4) == 192635
    assert solve() == 522095328


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
