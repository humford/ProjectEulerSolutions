import time


def coprimeToSixCount(n):
    if n <= 0:
        return 0
    return n - n // 2 - n // 3 + n // 6


def smoothTwoThreeUpTo(limit):
    values = []
    powerTwo = 1

    while powerTwo <= limit:
        powerThree = 1
        while powerTwo * powerThree <= limit:
            values.append(powerTwo * powerThree)
            powerThree *= 3
        powerTwo *= 2

    values.sort()
    return values


def holesUpTo(limit):
    holes = [value for value in (6, 24, 54) if value <= limit]

    value = 384
    while value <= limit:
        holes.append(value)
        value *= 8

    value = 243
    while value <= limit:
        holes.append(value)
        value *= 27

    holes.sort()
    return holes


def bestCoveredSmall(limit):
    values = smoothTwoThreeUpTo(limit)
    best = 0

    for mask in range(1 << len(values)):
        base = set()
        doubles = set()
        triples = set()
        ok = True

        for i, value in enumerate(values):
            if (mask >> i) & 1:
                double = 2 * value
                triple = 3 * value
                if (
                    value in doubles
                    or value in triples
                    or double in base
                    or double in triples
                    or triple in base
                    or triple in doubles
                ):
                    ok = False
                    break
                base.add(value)
                doubles.add(double)
                triples.add(triple)

        if ok:
            covered = sum(1 for value in base | doubles | triples if value <= limit)
            best = max(best, covered)

    return best


def F(n):
    smooth = smoothTwoThreeUpTo(n)
    smoothIndex = {value: index for index, value in enumerate(smooth)}

    smallH = {}
    for value in smooth:
        if value > 48:
            break
        smallH[value] = bestCoveredSmall(value)

    holes = holesUpTo(n)
    holePrefix = {}
    holeIndex = 0
    count = 0
    for value in smooth:
        while holeIndex < len(holes) and holes[holeIndex] <= value:
            count += 1
            holeIndex += 1
        holePrefix[value] = count

    def HAtSmoothBreakpoint(value):
        if value <= 48:
            return smallH[value]
        return smoothIndex[value] + 1 - holePrefix[value]

    total = 0
    for i, left in enumerate(smooth):
        right = n if i + 1 == len(smooth) else min(n, smooth[i + 1] - 1)

        lowK = n // (right + 1) + 1
        highK = n // left
        if lowK > highK:
            continue

        coprimeCount = coprimeToSixCount(highK) - coprimeToSixCount(lowK - 1)
        total += HAtSmoothBreakpoint(left) * coprimeCount

    return total


def runTests():
    assert F(6) == 5
    assert F(20) == 19


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = F(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
