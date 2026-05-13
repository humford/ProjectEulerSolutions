import math
import time


def oneLayerTriangles(n):
    return 3 * pow(4, n - 1) - 2 * pow(3, n - 1)


def threeLayerTriangles(n):
    powersOfFour = pow(4, n - 2)
    powersOfThree = pow(3, n - 1)
    return (18 * n - 138) * powersOfFour + (4 * n + 26) * powersOfThree


def snowflakeGcd(n):
    modulus = 7 * n + 3

    if n % 3:
        if modulus % 3 == 1:
            inverseOfThree = (2 * modulus + 1) // 3
        else:
            inverseOfThree = (modulus + 1) // 3

        base = (4 * inverseOfThree) % modulus
        residue = (2 * pow(base, n - 2, modulus) - 1) % modulus
    else:
        residue = (
            2 * pow(4, n - 2, modulus) - pow(3, n - 2, modulus)
        ) % modulus

    return 6 * math.gcd(residue, modulus)


def snowflakeGcdSum(limit):
    commonDivisorSum = 0
    gcd = math.gcd

    for n in range(4, limit + 1, 3):
        modulus = 7 * n + 3
        inverseOfThree = (2 * modulus + 1) // 3
        base = (4 * inverseOfThree) % modulus
        commonDivisorSum += gcd((2 * pow(base, n - 2, modulus) - 1) % modulus, modulus)

    for n in range(5, limit + 1, 3):
        modulus = 7 * n + 3
        inverseOfThree = (modulus + 1) // 3
        base = (4 * inverseOfThree) % modulus
        commonDivisorSum += gcd((2 * pow(base, n - 2, modulus) - 1) % modulus, modulus)

    for n in range(3, limit + 1, 3):
        modulus = 7 * n + 3
        residue = (
            2 * pow(4, n - 2, modulus) - pow(3, n - 2, modulus)
        ) % modulus
        commonDivisorSum += gcd(residue, modulus)

    return 6 * commonDivisorSum


def runTests():
    assert oneLayerTriangles(3) == 30
    assert threeLayerTriangles(3) == 6
    assert snowflakeGcd(3) == 6
    assert oneLayerTriangles(11) == 3_027_630
    assert threeLayerTriangles(11) == 19_862_070
    assert snowflakeGcd(11) == 30
    assert snowflakeGcd(500) == 186
    assert snowflakeGcdSum(500) == 5_124


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = snowflakeGcdSum(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
