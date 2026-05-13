import math
import time
from collections import defaultdict


LIMIT = 10 ** 7


def circumscribedCircleSumBrute(limit):
    total = 0
    maxSide = 2 * limit

    for a in range(1, maxSide + 1):
        for b in range(a, maxSide + 1):
            for c in range(b, min(maxSide, a + b - 1) + 1):
                perimeter = a + b + c
                area16 = (
                    perimeter
                    * (-a + b + c)
                    * (a - b + c)
                    * (a + b - c)
                )
                area4 = math.isqrt(area16)

                if area4 * area4 != area16:
                    continue

                numerator = a * b * c

                if numerator % area4 == 0:
                    radius = numerator // area4

                    if radius <= limit:
                        total += radius

    return total


def pythagoreanTangentsByRadius(limit):
    tangentsByRadius = defaultdict(set)
    maxDiameter = 2 * limit

    for m in range(2, math.isqrt(maxDiameter) + 2):
        for n in range(1, m):
            if (m - n) % 2 == 0 or math.gcd(m, n) != 1:
                continue

            hypotenuse = m * m + n * n
            if hypotenuse > maxDiameter:
                break

            common = math.gcd(m - n, m + n)
            tangents = (
                (n, m),
                (m, n),
                ((m - n) // common, (m + n) // common),
                ((m + n) // common, (m - n) // common),
            )
            step = hypotenuse if hypotenuse % 2 == 0 else 2 * hypotenuse
            start = step

            for diameter in range(start, maxDiameter + 1, step):
                tangentsByRadius[diameter // 2].update(tangents)

    return tangentsByRadius


def countTrianglesForRadius(radius, tangents):
    tangents.add((1, 1))
    orderedTangents = sorted(tangents, key=lambda tangent: tangent[0] / tangent[1])
    tangentSet = tangents
    count = 0

    for firstIndex, firstTangent in enumerate(orderedTangents):
        firstNumerator, firstDenominator = firstTangent

        for secondTangent in orderedTangents[firstIndex:]:
            secondNumerator, secondDenominator = secondTangent
            thirdNumerator = firstDenominator * secondDenominator - firstNumerator * secondNumerator

            if thirdNumerator <= 0:
                break

            thirdDenominator = (
                firstNumerator * secondDenominator
                + firstDenominator * secondNumerator
            )
            common = math.gcd(thirdNumerator, thirdDenominator)
            thirdTangent = (
                thirdNumerator // common,
                thirdDenominator // common,
            )

            if thirdTangent not in tangentSet:
                continue

            if secondNumerator * thirdTangent[1] > thirdTangent[0] * secondDenominator:
                continue

            count += 1

    return radius * count


def circumscribedCircleSum(limit=LIMIT):
    tangentsByRadius = pythagoreanTangentsByRadius(limit)
    return sum(
        countTrianglesForRadius(radius, tangents)
        for radius, tangents in tangentsByRadius.items()
    )


def runTests():
    assert circumscribedCircleSumBrute(100) == 4950
    assert circumscribedCircleSum(100) == 4950
    assert circumscribedCircleSum(1200) == 1653605


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = circumscribedCircleSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
