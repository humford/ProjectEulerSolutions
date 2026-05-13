import time
from array import array
from math import isqrt, log


def primeBound(count):
    if count < 6:
        return 15
    return int(count * (log(count) + log(log(count)))) + 10


def firstPrimes(count):
    limit = primeBound(count)

    while True:
        sieve = bytearray(b"\x01") * (limit // 2 + 1)
        sieve[0] = 0
        root = isqrt(limit)

        for index in range(1, root // 2 + 1):
            if sieve[index]:
                prime = 2 * index + 1
                start = prime * prime // 2
                sieve[start::prime] = b"\x00" * (
                    ((limit // 2 - start) // prime) + 1
                )

        primes = array("I", [2])
        appendPrime = primes.append
        for index in range(1, len(sieve)):
            if sieve[index]:
                appendPrime(2 * index + 1)
                if len(primes) == count:
                    return primes

        limit *= 2


def peakCoordinates(limit):
    primes = firstPrimes(2 * limit)
    xCoordinates = array("Q", [0])
    yCoordinates = array("Q", [0])
    x = 0
    y = 0
    appendX = xCoordinates.append
    appendY = yCoordinates.append
    primeIterator = iter(primes)

    for _ in range(limit):
        upSlope = next(primeIterator)
        x += upSlope
        y += upSlope
        appendX(x)
        appendY(y)

        downSlope = next(primeIterator)
        x += downSlope
        y -= downSlope

    return xCoordinates, yCoordinates


def candidateIsAboveSightLine(xCoordinates, yCoordinates, peak, current, candidate):
    yDifferenceCurrent = yCoordinates[peak] - yCoordinates[current]
    xDifferenceCurrent = xCoordinates[peak] - xCoordinates[current]

    return (
        (yCoordinates[peak] - yCoordinates[candidate]) * xDifferenceCurrent
        < yDifferenceCurrent * (xCoordinates[peak] - xCoordinates[candidate])
    )


def visibilityData(limit, requestedPeak=0):
    xCoordinates, yCoordinates = peakCoordinates(limit)
    offsets = array("I", [0])
    visibleEdges = array("I")
    total = 0
    requestedVisiblePeaks = []
    appendEdge = visibleEdges.append
    appendOffset = offsets.append

    for peak in range(1, limit + 1):
        start = len(visibleEdges)

        if peak > 1:
            current = peak - 1
            appendEdge(current)
            total += 1

            while current > 1:
                found = 0

                for position in range(offsets[current - 1], offsets[current]):
                    candidate = visibleEdges[position]
                    if candidateIsAboveSightLine(
                        xCoordinates, yCoordinates, peak, current, candidate
                    ):
                        found = candidate
                        break

                if not found:
                    break

                appendEdge(found)
                total += 1
                current = found

        appendOffset(len(visibleEdges))

        if peak == requestedPeak:
            requestedVisiblePeaks = list(visibleEdges[start : offsets[peak]])

    return total, requestedVisiblePeaks


def visiblePeakList(peak):
    return visibilityData(peak, peak)[1]


def visiblePeaks(peak):
    return len(visiblePeakList(peak))


def visiblePeakSum(limit):
    return visibilityData(limit)[0]


def visiblePeakListBrute(peak):
    xCoordinates, yCoordinates = peakCoordinates(peak)
    visible = []
    bestNumerator = None
    bestDenominator = None

    for candidate in range(peak - 1, 0, -1):
        numerator = yCoordinates[peak] - yCoordinates[candidate]
        denominator = xCoordinates[peak] - xCoordinates[candidate]

        if (
            bestNumerator is None
            or numerator * bestDenominator < bestNumerator * denominator
        ):
            visible.append(candidate)
            bestNumerator = numerator
            bestDenominator = denominator

    return visible


def visiblePeakSumBrute(limit):
    return sum(len(visiblePeakListBrute(peak)) for peak in range(1, limit + 1))


def runTests():
    assert visiblePeakList(3) == [2]
    assert visiblePeaks(3) == 1
    assert visiblePeakList(9) == [8, 7, 5]
    assert visiblePeaks(9) == 3
    assert visiblePeakSum(100) == 227
    assert visiblePeakSumBrute(100) == 227


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = visiblePeakSum(2_500_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
