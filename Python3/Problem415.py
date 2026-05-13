import time
from array import array
from functools import lru_cache


MODULUS = 10**8
DOUBLE_MODULUS = 2 * MODULUS
PREFIX_LIMIT = 10_000_000


def isTitanic(pointSet):
    points = list(pointSet)

    for index, first in enumerate(points):
        x1, y1 = first

        for second in points[index + 1 :]:
            x2, y2 = second
            count = 0

            for x, y in points:
                if (x2 - x1) * (y - y1) == (y2 - y1) * (x - x1):
                    count += 1

            if count == 2:
                return True

    return False


def bruteT(limit):
    points = [(x, y) for x in range(limit + 1) for y in range(limit + 1)]
    total = 0

    for mask in range(1, 1 << len(points)):
        subset = [points[index] for index in range(len(points)) if mask >> index & 1]

        if isTitanic(subset):
            total += 1

    return total


def powerSums(limit):
    firstPower = limit * (limit + 1) // 2
    secondPower = limit * (limit + 1) * (2 * limit + 1) // 6
    thirdPower = firstPower * firstPower

    return firstPower % MODULUS, secondPower % DOUBLE_MODULUS, thirdPower % MODULUS


class TitanicCounter:
    def __init__(self, prefixLimit):
        self.prefixLimit = prefixLimit
        self.phiPrefix, self.weightedPhiPrefix, self.squareWeightedPhiPrefix = (
            self.buildTotientPrefixes(prefixLimit)
        )

    def buildTotientPrefixes(self, limit):
        phi = array("I", range(limit + 1))

        if limit >= 1:
            phi[1] = 1

        for number in range(2, limit + 1):
            if phi[number] == number:
                for multiple in range(number, limit + 1, number):
                    phi[multiple] -= phi[multiple] // number

        phiPrefix = array("I", [0]) * (limit + 1)
        weightedPhiPrefix = array("I", [0]) * (limit + 1)
        squareWeightedPhiPrefix = array("I", [0]) * (limit + 1)

        phiTotal = 0
        weightedTotal = 0
        squareWeightedTotal = 0

        for number in range(1, limit + 1):
            phiValue = phi[number]
            phiTotal = (phiTotal + phiValue) % MODULUS
            weightedTotal = (weightedTotal + number * phiValue) % DOUBLE_MODULUS
            squareWeightedTotal = (
                squareWeightedTotal + (number * number % MODULUS) * phiValue
            ) % MODULUS

            phiPrefix[number] = phiTotal
            weightedPhiPrefix[number] = weightedTotal
            squareWeightedPhiPrefix[number] = squareWeightedTotal

        return phiPrefix, weightedPhiPrefix, squareWeightedPhiPrefix

    @lru_cache(maxsize=None)
    def totientSums(self, limit):
        if limit <= self.prefixLimit:
            return (
                self.phiPrefix[limit],
                self.weightedPhiPrefix[limit],
                self.squareWeightedPhiPrefix[limit],
            )

        phiTotal, weightedTotal, squareWeightedTotal = powerSums(limit)
        start = 1

        while start <= limit // 2:
            quotient = limit // start
            end = limit // quotient
            endSums = self.totientSums(end)

            if start == 1:
                phiRange, weightedRange, squareWeightedRange = endSums
            else:
                previousSums = self.totientSums(start - 1)
                phiRange = (endSums[0] - previousSums[0]) % MODULUS
                weightedRange = (endSums[1] - previousSums[1]) % DOUBLE_MODULUS
                squareWeightedRange = (endSums[2] - previousSums[2]) % MODULUS

            phiCoefficient = (quotient - 1) % MODULUS
            weightedCoefficient = (
                quotient * (quotient + 1) // 2 - 1
            ) % DOUBLE_MODULUS
            squareWeightedCoefficient = (
                quotient * (quotient + 1) * (2 * quotient + 1) // 6 - 1
            ) % MODULUS

            phiTotal = (phiTotal - phiCoefficient * phiRange) % MODULUS
            weightedTotal = (
                weightedTotal - weightedCoefficient * weightedRange
            ) % DOUBLE_MODULUS
            squareWeightedTotal = (
                squareWeightedTotal
                - squareWeightedCoefficient * squareWeightedRange
            ) % MODULUS

            start = end + 1

        return phiTotal, weightedTotal, squareWeightedTotal

    def primitiveDirectionSums(self, limit):
        if limit <= 0:
            return 0, 0, 0

        phiTotal, weightedTotal, squareWeightedTotal = self.totientSums(limit)
        primitivePairCount = (2 * phiTotal - 1) % MODULUS
        firstCoordinateSum = (1 + 3 * ((weightedTotal - 1) // 2)) % MODULUS

        return primitivePairCount, firstCoordinateSum, squareWeightedTotal

    def weightedPowerRange(self, start, end):
        endSums = self.weightedPowerPrefix(end)
        previousSums = self.weightedPowerPrefix(start - 1)
        exponentialSum = (endSums[0] - previousSums[0]) % MODULUS
        weightedExponentialSum = (endSums[1] - previousSums[1]) % MODULUS
        squareWeightedExponentialSum = (endSums[2] - previousSums[2]) % MODULUS

        count = (end - start + 1) % MODULUS
        plainWeightedSum = (
            end * (end + 1) // 2 - (start - 1) * start // 2
        ) % MODULUS
        plainSquareWeightedSum = (
            end * (end + 1) * (2 * end + 1) // 6
            - (start - 1) * start * (2 * start - 1) // 6
        ) % MODULUS

        return (
            (exponentialSum - count) % MODULUS,
            (weightedExponentialSum - plainWeightedSum) % MODULUS,
            (squareWeightedExponentialSum - plainSquareWeightedSum) % MODULUS,
        )

    def weightedPowerPrefix(self, limit):
        if limit <= 0:
            return 0, 0, 0

        power = pow(2, limit, MODULUS)

        return (
            (power - 1) % MODULUS,
            ((limit - 1) * power + 1) % MODULUS,
            ((limit * limit - 2 * limit + 3) * power - 3) % MODULUS,
        )

    def collinearSubsetCount(self, limit):
        sideLength = limit + 1
        slopeTotal = 0
        span = 2

        while span <= limit:
            directionLimit = limit // span
            endSpan = limit // directionLimit
            pairCount, coordinateSum, productSum = self.primitiveDirectionSums(
                directionLimit
            )
            constantTerm = sideLength * sideLength * pairCount % MODULUS
            linearTerm = 2 * sideLength * coordinateSum % MODULUS
            quadraticTerm = productSum
            powerSum, weightedPowerSum, squareWeightedPowerSum = (
                self.weightedPowerRange(span, endSpan)
            )

            slopeTotal = (
                slopeTotal
                + constantTerm * powerSum
                - linearTerm * weightedPowerSum
                + quadraticTerm * squareWeightedPowerSum
            ) % MODULUS
            span = endSpan + 1

        axisTotal = (
            2 * sideLength * self.collinearSubsetCountOnOneLine(sideLength)
        ) % MODULUS

        return (axisTotal + 2 * slopeTotal) % MODULUS

    def collinearSubsetCountOnOneLine(self, pointCount):
        return (
            pow(2, pointCount, MODULUS)
            - 1
            - pointCount
            - pointCount * (pointCount - 1) // 2
        ) % MODULUS

    def titanicSetCount(self, limit):
        pointCount = (limit + 1) ** 2
        totalSubsets = (pow(2, pointCount, MODULUS) - 1 - pointCount) % MODULUS

        return (totalSubsets - self.collinearSubsetCount(limit)) % MODULUS


def runTests(counter):
    assert bruteT(1) == 11
    assert bruteT(2) == 494
    assert counter.titanicSetCount(4) == 33554178
    assert counter.titanicSetCount(111) == 13500401
    assert counter.titanicSetCount(10**5) == 63259062


if __name__ == "__main__":
    start = time.time()
    counter = TitanicCounter(PREFIX_LIMIT)
    runTests(counter)
    answer = counter.titanicSetCount(10**11)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
