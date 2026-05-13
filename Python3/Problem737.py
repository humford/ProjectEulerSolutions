import math
import time
from array import array


EULER_GAMMA_TERMS = 2_000_000
PREFIX_TERMS = 500_000


def computeEulerGamma(termCount=EULER_GAMMA_TERMS):
    harmonic = 0.0
    for denominator in range(1, termCount + 1):
        harmonic += 1.0 / denominator

    inverse = 1.0 / termCount
    inverse2 = inverse * inverse
    inverse4 = inverse2 * inverse2
    inverse6 = inverse4 * inverse2
    inverse8 = inverse4 * inverse4
    return (
        harmonic
        - math.log(termCount)
        - 0.5 * inverse
        + (1.0 / 12.0) * inverse2
        - (1.0 / 120.0) * inverse4
        + (1.0 / 252.0) * inverse6
        - (1.0 / 240.0) * inverse8
    )


EULER_GAMMA = computeEulerGamma()


def harmonicAsymptotic(value):
    inverse = 1.0 / value
    inverse2 = inverse * inverse
    inverse4 = inverse2 * inverse2
    inverse6 = inverse4 * inverse2
    inverse8 = inverse4 * inverse4
    return (
        math.log(value)
        + EULER_GAMMA
        + 0.5 * inverse
        - (1.0 / 12.0) * inverse2
        + (1.0 / 120.0) * inverse4
        - (1.0 / 252.0) * inverse6
        + (1.0 / 240.0) * inverse8
    )


def gaussLegendreNodesAndWeights(order):
    nodes = [0.0] * order
    weights = [0.0] * order
    rootCount = (order + 1) // 2

    for index in range(1, rootCount + 1):
        node = math.cos(math.pi * (index - 0.25) / (order + 0.5))

        for _ in range(50):
            current = 1.0
            previous = 0.0
            for degree in range(1, order + 1):
                beforePrevious = previous
                previous = current
                current = ((2.0 * degree - 1.0) * node * previous - (degree - 1.0) * beforePrevious) / degree
            derivative = order * (node * current - previous) / (node * node - 1.0)
            nextNode = node - current / derivative
            if abs(nextNode - node) < 1e-15:
                node = nextNode
                break
            node = nextNode

        current = 1.0
        previous = 0.0
        for degree in range(1, order + 1):
            beforePrevious = previous
            previous = current
            current = ((2.0 * degree - 1.0) * node * previous - (degree - 1.0) * beforePrevious) / degree
        derivative = order * (node * current - previous) / (node * node - 1.0)
        weight = 2.0 / ((1.0 - node * node) * derivative * derivative)

        nodes[index - 1] = -node
        nodes[order - index] = node
        weights[index - 1] = weight
        weights[order - index] = weight

    return nodes, weights


def betaFromHarmonicIndex(index, harmonic):
    centerMassRadius = math.sqrt(harmonic / index)
    ratio = math.sqrt(1.0 - 0.25 * centerMassRadius * centerMassRadius) / (
        centerMassRadius * (index + 0.5)
    )
    return math.atan(ratio)


def betaReal(coinCount):
    index = coinCount - 1.0
    return betaFromHarmonicIndex(index, harmonicAsymptotic(index))


def alphaFromHarmonicIndex(index, harmonic):
    centerMassRadius = math.sqrt(harmonic / index)
    return math.acos(0.5 * centerMassRadius)


def integrateBetaLog(start, stop, nodes, weights, logSegmentSize=0.5):
    if stop <= start:
        return 0.0

    logStart = math.log(start)
    logStop = math.log(stop)
    segmentCount = max(1, int(math.ceil((logStop - logStart) / logSegmentSize)))
    segmentWidth = (logStop - logStart) / segmentCount

    total = 0.0
    for segment in range(segmentCount):
        left = logStart + segment * segmentWidth
        right = left + segmentWidth
        middle = 0.5 * (left + right)
        halfWidth = 0.5 * (right - left)

        segmentTotal = 0.0
        for node, weight in zip(nodes, weights):
            logCoinCount = middle + halfWidth * node
            coinCount = math.exp(logCoinCount)
            segmentTotal += weight * betaReal(coinCount) * coinCount
        total += segmentTotal * halfWidth

    return total


class CoinLoopsSolver:
    def __init__(self, prefixTerms=PREFIX_TERMS, quadratureOrder=16):
        self.prefixTerms = max(10_000, int(prefixTerms))
        self.nodes, self.weights = gaussLegendreNodesAndWeights(int(quadratureOrder))

        self.harmonicPrefix = array("d", [0.0]) * (self.prefixTerms + 1)
        self.betaPrefix = array("d", [0.0]) * (self.prefixTerms + 1)

        harmonic = 0.0
        for index in range(1, self.prefixTerms + 1):
            harmonic += 1.0 / index
            self.harmonicPrefix[index] = harmonic

        betaTotal = 0.0
        for coinCount in range(2, self.prefixTerms + 1):
            index = coinCount - 1
            betaTotal += betaFromHarmonicIndex(float(index), self.harmonicPrefix[index])
            self.betaPrefix[coinCount] = betaTotal

    def harmonic(self, index):
        if index <= self.prefixTerms:
            return self.harmonicPrefix[index]
        return harmonicAsymptotic(float(index))

    def alpha(self, coinCount):
        if coinCount <= 1:
            return 0.0
        index = coinCount - 1
        return alphaFromHarmonicIndex(float(index), self.harmonic(index))

    def betaTailSum(self, start, stop):
        if stop < start:
            return 0.0
        integral = integrateBetaLog(float(start), float(stop), self.nodes, self.weights)
        return integral + 0.5 * (betaReal(float(start)) + betaReal(float(stop)))

    def rotationSum(self, coinCount):
        if coinCount < 2:
            return 0.0

        if coinCount <= self.prefixTerms + 1:
            return self.alpha(coinCount) + self.betaPrefix[coinCount - 1]

        return (
            self.alpha(coinCount)
            + self.betaPrefix[self.prefixTerms]
            + self.betaTailSum(self.prefixTerms + 1, coinCount - 1)
        )

    def minimumCoinsForLoops(self, loopCount):
        if loopCount <= 0:
            return 1

        target = 2.0 * math.pi * loopCount
        low = 1
        high = max(2, 5 * loopCount)

        while self.rotationSum(high) <= target:
            high *= 2

        while low + 1 < high:
            middle = (low + high) // 2
            if self.rotationSum(middle) > target:
                high = middle
            else:
                low = middle

        return high


def runTests():
    solver = CoinLoopsSolver()
    assert solver.minimumCoinsForLoops(1) == 31
    assert solver.minimumCoinsForLoops(2) == 154
    assert solver.minimumCoinsForLoops(10) == 6_947


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = CoinLoopsSolver().minimumCoinsForLoops(2020)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
