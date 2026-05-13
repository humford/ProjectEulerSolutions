import math
import time


MODULUS = 1_000_000_007


def easyPizzaPrefix(limit, modulus=None):
    if limit < 3:
        return 0

    numerator = limit ** 3 + 15 * limit ** 2 - 52 * limit + 36
    value = numerator // 6
    return value if modulus is None else value % modulus


def minimumHardCutCount(x, y):
    fourDiscriminant = 4 * x * (x + 1) * y * (y + 1)
    root = math.isqrt(fourDiscriminant)
    if root * root == fourDiscriminant:
        ceiling = root
        isSquare = 1
    else:
        ceiling = root + 1
        isSquare = 0

    return 2 * x * y + x + y + 1 + ceiling, isSquare


def maximumY(limit, x):
    if 4 * x > limit - 1:
        return x - 1

    low = x
    high = max(x, (limit - 1) // (4 * x) + 2)
    best = x - 1

    while low <= high:
        middle = (low + high) // 2
        minimumN, _ = minimumHardCutCount(x, middle)
        if minimumN <= limit:
            best = middle
            low = middle + 1
        else:
            high = middle - 1

    return best


def hardPizzaPrefixOneCorner(limit, modulus=None):
    if limit < 3:
        return 0

    xLimit = math.isqrt((limit - 1) // 4)
    total = 0
    cutoff = 0 if modulus is None else modulus << 20

    for x in range(1, xLimit + 1):
        yLimit = maximumY(limit, x)
        if yLimit < x:
            continue

        xFactor = x * (x + 1)
        y = x
        yFactor = y * (y + 1)
        twoXY = 2 * x * y

        while y <= yLimit:
            fourDiscriminant = (xFactor * yFactor) << 2
            root = math.isqrt(fourDiscriminant)
            if root * root == fourDiscriminant:
                ceiling = root
                isSquare = 1
            else:
                ceiling = root + 1
                isSquare = 0

            minimumN = twoXY + x + y + 1 + ceiling
            if minimumN <= limit:
                contribution = 2 * (limit - minimumN + 1) - isSquare
                total += contribution if x == y else 2 * contribution
                if modulus is not None and total >= cutoff:
                    total %= modulus

            yFactor += 2 * y + 2
            y += 1
            twoXY += 2 * x

    return total if modulus is None else total % modulus


def pizzaPrefix(limit, modulus=MODULUS):
    easy = easyPizzaPrefix(limit, modulus)
    hard = hardPizzaPrefixOneCorner(limit, modulus)
    if modulus is None:
        return easy + 3 * hard
    return (easy + 3 * hard) % modulus


def pizzaCutCount(n):
    if n < 3:
        return 0
    return pizzaPrefix(n, None) - pizzaPrefix(n - 1, None)


def runTests():
    assert pizzaCutCount(3) == 7
    assert pizzaCutCount(6) == 34
    assert pizzaCutCount(10) == 90
    assert pizzaPrefix(10, None) == 345
    assert pizzaPrefix(1_000, None) == 172_166_601


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pizzaPrefix(10 ** 8, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
