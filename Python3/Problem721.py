import time


MODULUS = 999_999_937


def quadraticPowerRealPart(ceilingRoot, radicand, exponent, modulus):
    realPart = ceilingRoot % modulus
    irrationalPart = 1
    radicand %= modulus

    for bit in bin(exponent)[3:]:
        nextReal = (realPart * realPart + radicand * irrationalPart * irrationalPart) % modulus
        nextIrrational = (2 * realPart * irrationalPart) % modulus
        realPart, irrationalPart = nextReal, nextIrrational

        if bit == "1":
            nextReal = (ceilingRoot * realPart + radicand * irrationalPart) % modulus
            nextIrrational = (realPart + ceilingRoot * irrationalPart) % modulus
            realPart, irrationalPart = nextReal, nextIrrational

    return realPart


def irrationalPowerFloor(a, exponent, modulus=MODULUS):
    ceilingRoot = 1
    while ceilingRoot * ceilingRoot < a:
        ceilingRoot += 1

    realPart = quadraticPowerRealPart(ceilingRoot, a, exponent, modulus)
    result = 2 * realPart
    if ceilingRoot * ceilingRoot != a:
        result -= 1
    return result % modulus


def irrationalPowerSum(limit, modulus=MODULUS):
    total = 0
    ceilingRoot = 1
    ceilingRootSquare = 1

    for a in range(1, limit + 1):
        if a > ceilingRootSquare:
            ceilingRoot += 1
            ceilingRootSquare = ceilingRoot * ceilingRoot

        realPart = quadraticPowerRealPart(ceilingRoot, a, a * a, modulus)
        contribution = 2 * realPart
        if a != ceilingRootSquare:
            contribution -= 1

        total = (total + contribution) % modulus

    return total


def runTests():
    assert irrationalPowerFloor(5, 2) == 27
    assert irrationalPowerFloor(5, 5) == 3_935
    assert irrationalPowerFloor(4, 3) == 64
    assert irrationalPowerSum(1_000) == 163_861_845


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = irrationalPowerSum(5_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
