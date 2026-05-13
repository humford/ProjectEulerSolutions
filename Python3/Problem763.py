import time
from array import array


MOD = 1_000_000_000


def makeStorage(size, modulus):
    if modulus is None:
        return [0] * size
    return array("I", [0]) * size


def reduceValue(value, modulus):
    return value if modulus is None else value % modulus


def computeA2(maxIndex, modulus=None):
    # a2[m] is D(m + 1), so D(10000) is a2[9999].
    nTemp = 0
    while (nTemp + 1) * (nTemp + 2) // 2 <= maxIndex:
        nTemp += 1
    maxN = nTemp - 1
    tableSize = maxN + 3

    offset = [0] * (tableSize + 2)
    lengths = [0] * (tableSize + 2)
    for n in range(tableSize + 2):
        currentOffset = (n + 1) * (n + 2) // 2
        offset[n] = currentOffset
        lengths[n] = max(0, maxIndex - currentOffset + 1)

    u = [[] for _ in range(tableSize + 2)]
    v = [[] for _ in range(tableSize + 2)]
    for n in range(1, tableSize + 2):
        length = lengths[n]
        if length > 0:
            u[n] = makeStorage(n * length, modulus)
            v[n] = makeStorage(n * length, modulus)

    f0 = makeStorage(maxIndex + 1, modulus)
    a2 = makeStorage(maxIndex + 1, modulus)
    a2[0] = 1

    activeN = 0
    for m in range(maxIndex + 1):
        while activeN + 1 < tableSize + 1 and offset[activeN + 1] <= m:
            activeN += 1

        for n in range(1, activeN + 1):
            currentOffset = offset[n]
            length = lengths[n]
            currentIndex = m - currentOffset

            m1 = m - n - 2
            index1 = m1 - currentOffset

            m2 = m - n - 3
            index2 = m2 - offset[n + 1]
            nextLength = lengths[n + 1]

            m3 = m - n - 1
            index3 = m3 - offset[n - 1]
            previousLength = lengths[n - 1]

            if n == 1:
                valueU = 0
                if index1 >= 0:
                    valueU += 2 * u[1][index1] + v[1][index1]
                if index2 >= 0 and nextLength > 0:
                    valueU += v[2][index2] + u[2][nextLength + index2]
                if m3 >= 0:
                    valueU += f0[m3]
                u[1][currentIndex] = reduceValue(valueU, modulus)

                valueV = 0
                if index1 >= 0:
                    valueV += 2 * v[1][index1] + 2 * u[1][index1]
                if index2 >= 0 and nextLength > 0:
                    valueV += v[2][nextLength + index2] + 2 * u[2][index2]
                if m3 >= 0:
                    valueV += f0[m3]
                v[1][currentIndex] = reduceValue(valueV, modulus)
                continue

            currentU = u[n]
            currentV = v[n]
            nextU = u[n + 1]
            nextV = v[n + 1]
            previousU = u[n - 1]
            previousV = v[n - 1]

            uN1 = currentU[index1] if index1 >= 0 else 0
            vN1 = currentV[index1] if index1 >= 0 else 0
            uP1 = nextU[index2] if index2 >= 0 and nextLength > 0 else 0
            vP1 = nextV[index2] if index2 >= 0 and nextLength > 0 else 0

            base = 0
            nextBase = length
            baseNext = nextLength
            basePrevious = 0

            if index1 < 0:
                for _ in range(1, n):
                    currentU[base + currentIndex] = previousU[basePrevious + index3]
                    currentV[base + currentIndex] = previousV[basePrevious + index3]
                    base = nextBase
                    nextBase += length
                    basePrevious += previousLength

                lastBase = (n - 1) * length
                previousLastBase = (n - 2) * previousLength
                currentU[lastBase + currentIndex] = previousU[previousLastBase + index3]
                currentV[lastBase + currentIndex] = previousV[previousLastBase + index3]
                continue

            if index2 >= 0 and nextLength > 0:
                for _ in range(1, n):
                    currentU[base + currentIndex] = reduceValue(
                        currentU[base + index1]
                        + vP1
                        + nextU[baseNext + index2]
                        + previousU[basePrevious + index3]
                        + vN1
                        + currentU[nextBase + index1],
                        modulus,
                    )
                    currentV[base + currentIndex] = reduceValue(
                        currentV[base + index1]
                        + nextV[baseNext + index2]
                        + uP1
                        + previousV[basePrevious + index3]
                        + currentV[nextBase + index1]
                        + uN1,
                        modulus,
                    )
                    base = nextBase
                    nextBase += length
                    baseNext += nextLength
                    basePrevious += previousLength

                lastBase = (n - 1) * length
                previousLastBase = (n - 2) * previousLength
                currentU[lastBase + currentIndex] = reduceValue(
                    2 * currentU[lastBase + index1]
                    + vN1
                    + vP1
                    + nextU[baseNext + index2]
                    + previousU[previousLastBase + index3],
                    modulus,
                )
                currentV[lastBase + currentIndex] = reduceValue(
                    2 * currentV[lastBase + index1]
                    + 2 * uN1
                    + nextV[baseNext + index2]
                    + 2 * uP1
                    + previousV[previousLastBase + index3],
                    modulus,
                )
            else:
                for _ in range(1, n):
                    currentU[base + currentIndex] = reduceValue(
                        currentU[base + index1]
                        + previousU[basePrevious + index3]
                        + vN1
                        + currentU[nextBase + index1],
                        modulus,
                    )
                    currentV[base + currentIndex] = reduceValue(
                        currentV[base + index1]
                        + previousV[basePrevious + index3]
                        + currentV[nextBase + index1]
                        + uN1,
                        modulus,
                    )
                    base = nextBase
                    nextBase += length
                    basePrevious += previousLength

                lastBase = (n - 1) * length
                previousLastBase = (n - 2) * previousLength
                currentU[lastBase + currentIndex] = reduceValue(
                    2 * currentU[lastBase + index1]
                    + vN1
                    + previousU[previousLastBase + index3],
                    modulus,
                )
                currentV[lastBase + currentIndex] = reduceValue(
                    2 * currentV[lastBase + index1]
                    + 2 * uN1
                    + previousV[previousLastBase + index3],
                    modulus,
                )

        valueF = 0
        if m - 1 >= 0:
            valueF += a2[m - 1]
        if m - 2 >= 0:
            valueF += 4 * f0[m - 2]
        previousM = m - 3
        if previousM >= offset[1] and lengths[1] > 0:
            index = previousM - offset[1]
            valueF += 2 * u[1][index] + v[1][index]
        f0[m] = reduceValue(valueF, modulus)

        if m >= 1:
            valueA = 3 * a2[m - 1]
            if m - 2 >= 0:
                valueA += 3 * f0[m - 2]
            a2[m] = reduceValue(valueA, modulus)

    return a2


def bruteCounts(maxDivisions):
    arrangements = {frozenset({(0, 0, 0)})}
    counts = [1]
    for _ in range(maxDivisions):
        nextArrangements = set()
        for arrangement in arrangements:
            occupied = set(arrangement)
            for x, y, z in arrangement:
                children = ((x + 1, y, z), (x, y + 1, z), (x, y, z + 1))
                if any(child in occupied for child in children):
                    continue
                newArrangement = set(occupied)
                newArrangement.remove((x, y, z))
                newArrangement.update(children)
                nextArrangements.add(frozenset(newArrangement))
        arrangements = nextArrangements
        counts.append(len(arrangements))
    return counts


def D(divisions, modulus=None):
    if divisions == 0:
        return 1
    return computeA2(divisions - 1, modulus)[divisions - 1]


def runTests():
    exact = computeA2(19)
    brute = bruteCounts(7)
    for divisions in range(1, 8):
        assert exact[divisions - 1] == brute[divisions]

    assert exact[1] == 3
    assert exact[9] == 44_499
    assert exact[19] == 9_204_559_704
    assert computeA2(99, MOD)[99] == 780_166_455


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = computeA2(9_999, MOD)[9_999]
    elapsed = time.time() - start

    print("Found " + f"{answer:09d}" + " in " + str(elapsed) + " seconds.")
