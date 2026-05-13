from array import array
import math
import time


PROBLEM_LIMIT = 10**7


def buildPythagoreanPairs(maxInradius, maxTangentLength):
    counts = array("I", [0]) * (maxInradius + 1)
    gcd = math.gcd
    mLimit = math.isqrt(maxTangentLength) + 1

    for m in range(2, mLimit + 1):
        mSquared = m * m
        for n in range(1, m):
            if ((m - n) & 1) == 0 or gcd(m, n) != 1:
                continue

            legA = mSquared - n * n
            legB = 2 * m * n
            if legA > legB:
                legA, legB = legB, legA

            maxScale = min(maxInradius // legA, maxTangentLength // legB)
            for inradius in range(legA, legA * (maxScale + 1), legA):
                counts[inradius] += 1

            maxScale = min(maxInradius // legB, maxTangentLength // legA)
            for inradius in range(legB, legB * (maxScale + 1), legB):
                counts[inradius] += 1

    offsets = array("I", [0]) * (maxInradius + 2)
    total = 0
    for inradius in range(1, maxInradius + 1):
        total += counts[inradius]
        offsets[inradius + 1] = total

    tangentLengths = array("I", [0]) * total
    incenterDistances = array("I", [0]) * total
    positions = array("I", offsets)

    for m in range(2, mLimit + 1):
        mSquared = m * m
        for n in range(1, m):
            if ((m - n) & 1) == 0 or gcd(m, n) != 1:
                continue

            legA = mSquared - n * n
            legB = 2 * m * n
            if legA > legB:
                legA, legB = legB, legA
            hypotenuse = mSquared + n * n

            maxScale = min(maxInradius // legA, maxTangentLength // legB)
            for scale in range(1, maxScale + 1):
                inradius = scale * legA
                index = positions[inradius]
                tangentLengths[index] = scale * legB
                incenterDistances[index] = scale * hypotenuse
                positions[inradius] = index + 1

            maxScale = min(maxInradius // legB, maxTangentLength // legA)
            for scale in range(1, maxScale + 1):
                inradius = scale * legB
                index = positions[inradius]
                tangentLengths[index] = scale * legA
                incenterDistances[index] = scale * hypotenuse
                positions[inradius] = index + 1

    return offsets, tangentLengths, incenterDistances


def incenterTriangleSum(perimeterLimit):
    semiperimeterLimit = perimeterLimit // 2
    if semiperimeterLimit < 3:
        return 0

    maxTangentLength = semiperimeterLimit - 2
    maxInradius = int(semiperimeterLimit * math.sqrt(3) / 9) + 2
    offsets, tangentLengths, incenterDistances = buildPythagoreanPairs(
        maxInradius, maxTangentLength
    )

    total = 0
    for inradius in range(1, maxInradius + 1):
        start = offsets[inradius]
        end = offsets[inradius + 1]
        if end - start < 3:
            continue

        distancesByTangent = {}
        for index in range(start, end):
            distancesByTangent[tangentLengths[index]] = incenterDistances[index]
        if len(distancesByTangent) < 3:
            continue

        tangents = sorted(distancesByTangent)
        inradiusSquared = inradius * inradius
        getDistance = distancesByTangent.get

        for xIndex, x in enumerate(tangents):
            distanceX = distancesByTangent[x]
            for y in tangents[xIndex:]:
                denominator = x * y - inradiusSquared
                if denominator <= 0:
                    continue

                numerator = inradiusSquared * (x + y)
                if numerator % denominator:
                    continue

                z = numerator // denominator
                if z < y:
                    continue

                semiperimeter = x + y + z
                if semiperimeter > semiperimeterLimit:
                    continue

                distanceZ = getDistance(z)
                if distanceZ is None:
                    continue

                total += (
                    2 * semiperimeter
                    + distanceX
                    + distancesByTangent[y]
                    + distanceZ
                )

    return total


def runTests():
    assert incenterTriangleSum(10**3) == 3_619


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = incenterTriangleSum(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
