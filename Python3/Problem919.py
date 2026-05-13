from math import gcd, isqrt
import time


TARGET_PERIMETER = 10_000_000
PARAMETER_GCD_BOUND = 30

# If A is the tested vertex, then AH = 2R|cos(A)| and AO = R, so a
# fortunate angle has cos(A) = +/- 1/4.  With adjacent sides y,z and
# opposite side x:
#
#     x^2 = y^2 + z^2 - sign * y*z/2,  sign in {1, -1}.
#
# Parameterizing this conic from the degenerate rational point (z/y, x/y)
# = (0, 1) gives, for coprime integers m,n and z <= y:
#
#     x = 2n^2 + 2m^2 + sign*m*n
#     y = 2(n^2 - m^2)
#     z = n(4m + sign*n)
#
# For coprime m,n the common divisor of x,y,z divides 30: any odd prime
# divisor must satisfy 16 == 1 modulo p, hence p is 3 or 5, and the
# 2-adic valuation is at most one.  This bounds the raw-parameter search
# needed to find every primitive triangle with perimeter <= TARGET.


def encodeTriangle(a, b, c, base):
    if a > b:
        a, b = b, a
    if b > c:
        b, c = c, b
    if a > b:
        a, b = b, a

    return (a * base + b) * base + c


def perimeterFromCode(code, base):
    c = code % base
    code //= base
    b = code % base
    a = code // base
    return a + b + c


def primitiveFortunateTriangles(perimeterLimit):
    base = perimeterLimit + 1
    rawLimit = PARAMETER_GCD_BOUND * perimeterLimit
    nLimit = isqrt(8 * perimeterLimit) + 3
    triangles = set()

    for sign, perimeterFactor in ((1, 5), (-1, 3)):
        for n in range(1, nLimit + 1):
            if sign == 1:
                mMin = (-n) // 4 + 1
                while 4 * mMin + n <= 0:
                    mMin += 1
            else:
                mMin = n // 4 + 1
                while 4 * mMin - n <= 0:
                    mMin += 1

            for m in range(mMin, n):
                rawPerimeter = perimeterFactor * n * (n + m)
                if rawPerimeter > rawLimit:
                    break

                adjacentLong = 2 * (n * n - m * m)
                adjacentShort = n * (4 * m + sign * n)
                if adjacentShort > adjacentLong:
                    break

                if gcd(abs(m), n) != 1:
                    continue

                opposite = 2 * n * n + 2 * m * m + sign * m * n
                common = gcd(gcd(opposite, adjacentLong), adjacentShort)
                primitivePerimeter = rawPerimeter // common

                if primitivePerimeter <= perimeterLimit:
                    triangles.add(encodeTriangle(
                        opposite // common,
                        adjacentLong // common,
                        adjacentShort // common,
                        base,
                    ))

    return triangles


def S(perimeterLimit):
    base = perimeterLimit + 1
    total = 0

    for code in primitiveFortunateTriangles(perimeterLimit):
        perimeter = perimeterFromCode(code, base)
        multipleCount = perimeterLimit // perimeter
        total += perimeter * multipleCount * (multipleCount + 1) // 2

    return total


def isFortunateTriangle(a, b, c):
    if a + b <= c:
        return False

    sides = (a, b, c)
    for index, opposite in enumerate(sides):
        adjacent = [sides[i] for i in range(3) if i != index]
        numerator = adjacent[0] * adjacent[0] + adjacent[1] * adjacent[1] - opposite * opposite
        if abs(2 * numerator) == adjacent[0] * adjacent[1]:
            return True

    return False


def bruteS(perimeterLimit):
    total = 0
    for a in range(1, perimeterLimit // 3 + 1):
        for b in range(a, (perimeterLimit - a) // 2 + 1):
            for c in range(b, perimeterLimit - a - b + 1):
                if isFortunateTriangle(a, b, c):
                    total += a + b + c
    return total


def solve():
    return S(TARGET_PERIMETER)


def runTests():
    assert isFortunateTriangle(1, 2, 2)
    assert isFortunateTriangle(2, 3, 4)
    assert isFortunateTriangle(2, 4, 4)
    assert isFortunateTriangle(6, 7, 8)
    assert bruteS(10) == 24
    assert S(10) == 24
    assert bruteS(100) == 3331
    assert S(100) == 3331
    assert solve() == 134_222_859_969_633


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
