import time


def nextMirrorPowerTerm(value, n, exponent):
    powered = value ** exponent
    return min(powered, n - powered)


def integerRoot(n, exponent):
    if exponent == 1:
        return n

    low = 1
    high = 2
    while high ** exponent <= n:
        high *= 2

    while low < high:
        middle = (low + high + 1) // 2
        if middle ** exponent <= n:
            low = middle
        else:
            high = middle - 1
    return low


def maxBaseForPowerSum(limit, highExponent, lowExponent):
    low = 1
    high = integerRoot(limit, highExponent)
    while low < high:
        middle = (low + high + 1) // 2
        if middle ** highExponent + middle ** lowExponent <= limit:
            low = middle
        else:
            high = middle - 1
    return low


def isExactPower(value, exponent):
    root = integerRoot(value, exponent)
    return root >= 2 and root ** exponent == value


def bruteMirrorPowerSequenceTotal(limit):
    total = 0
    for n in range(2, limit + 1):
        exponent = 2
        while 2 ** exponent < n - 1:
            maxStart = integerRoot(n - 2, exponent)
            for start in range(2, maxStart + 1):
                value = start
                seen = set()
                while value > 1 and value not in seen:
                    seen.add(value)
                    powered = value ** exponent
                    if powered >= n - 1:
                        value = 0
                    else:
                        value = min(powered, n - powered)
                if value > 1:
                    total += 1
            exponent += 1
    return total


def mirrorPowerSequenceTotal(limit):
    total = 0
    exponent = 2

    while 2 ** exponent + 2 <= limit:
        fixedPointMax = maxBaseForPowerSum(limit, exponent, 1)
        if fixedPointMax >= 2:
            total += fixedPointMax - 1
            total -= max(0, integerRoot(fixedPointMax, exponent) - 1)

        chainLength = 2
        while True:
            highExponent = exponent ** chainLength
            if 2 ** highExponent + 2 > limit:
                break

            maxBase = integerRoot(limit, highExponent)
            for base in range(2, maxBase + 1):
                if isExactPower(base, exponent):
                    continue

                highPower = base ** highExponent
                for lowIndex in range(chainLength):
                    lowExponent = exponent ** lowIndex
                    if highPower + base ** lowExponent <= limit:
                        total += chainLength

            chainLength += 1

        exponent += 1

    return total


def runTests():
    assert nextMirrorPowerTerm(2, 18, 2) == 4
    assert nextMirrorPowerTerm(4, 18, 2) == 2
    assert bruteMirrorPowerSequenceTotal(100) == 21
    assert mirrorPowerSequenceTotal(10) == 2
    assert mirrorPowerSequenceTotal(100) == 21
    assert mirrorPowerSequenceTotal(1_000) == 69
    assert mirrorPowerSequenceTotal(10 ** 6) == 1_303
    assert mirrorPowerSequenceTotal(10 ** 12) == 1_014_800


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = mirrorPowerSequenceTotal(10 ** 18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
