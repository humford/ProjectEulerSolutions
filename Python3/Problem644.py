import bisect
import math
import time


SQRT_TWO = math.sqrt(2.0)
EPSILON = 1e-12


def latticeBreakpoints(maxLength):
    values = [0.0]
    maxDiagonalCount = int(maxLength / SQRT_TWO) + 1
    for diagonalCount in range(maxDiagonalCount + 1):
        diagonalLength = diagonalCount * SQRT_TWO
        maxStraightCount = int(maxLength - diagonalLength + EPSILON)
        for straightCount in range(maxStraightCount + 1):
            values.append(straightCount + diagonalLength)
    return sorted(set(values))


def mex(values):
    result = 0
    while result in values:
        result += 1
    return result


def grundyIntervals(maxLength):
    boundaries = latticeBreakpoints(maxLength)
    starts = []
    ends = []
    grundyValues = []
    maxSeenGrundy = 0

    for boundaryIndex in range(len(boundaries) - 1):
        left = boundaries[boundaryIndex]
        right = boundaries[boundaryIndex + 1]
        segmentLength = (left + right) / 2
        reachable = set()

        for squareLength in (1.0, SQRT_TWO):
            if segmentLength < squareLength or not starts:
                continue

            splitTotal = segmentLength - squareLength
            lowerIndex = 0
            upperIndex = bisect.bisect_right(starts, splitTotal) - 1

            while lowerIndex <= upperIndex:
                lowerStart = starts[lowerIndex]
                if lowerStart >= splitTotal:
                    break

                lowerEnd = min(ends[lowerIndex], splitTotal)
                upperStart = starts[upperIndex]
                upperEnd = min(ends[upperIndex], splitTotal)

                overlapStart = max(lowerStart, splitTotal - upperEnd)
                overlapEnd = min(lowerEnd, splitTotal - upperStart)
                if overlapStart < overlapEnd:
                    reachable.add(
                        grundyValues[lowerIndex] ^ grundyValues[upperIndex]
                    )

                if lowerEnd < splitTotal - upperStart:
                    lowerIndex += 1
                else:
                    upperIndex -= 1

        value = mex(reachable)
        maxSeenGrundy = max(maxSeenGrundy, value)
        if grundyValues and grundyValues[-1] == value and abs(ends[-1] - left) < EPSILON:
            ends[-1] = right
        else:
            starts.append(left)
            ends.append(right)
            grundyValues.append(value)

    return starts, ends, grundyValues


def winningMeasureSegments(starts, ends, grundyValues, maxSplitTotal):
    maxGrundy = max(grundyValues)
    groups = [[] for _ in range(maxGrundy + 1)]
    for start, end, grundyValue in zip(starts, ends, grundyValues):
        groups[grundyValue].append((start, end))

    events = []
    for intervals in groups:
        for leftIndex, (leftStart, leftEnd) in enumerate(intervals):
            for rightIndex in range(leftIndex, len(intervals)):
                rightStart, rightEnd = intervals[rightIndex]
                weight = 1 if leftIndex == rightIndex else 2

                start = leftStart + rightStart
                risingEnd = min(leftStart + rightEnd, leftEnd + rightStart)
                fallingStart = max(leftStart + rightEnd, leftEnd + rightStart)
                end = leftEnd + rightEnd

                if start > maxSplitTotal + EPSILON:
                    break
                if end < 0:
                    continue

                start = max(start, 0.0)
                end = min(end, maxSplitTotal)
                events.append((start, weight))
                events.append((risingEnd, -weight))
                events.append((fallingStart, -weight))
                events.append((end, weight))

    events.sort()

    mergedEvents = []
    for position, delta in events:
        if mergedEvents and abs(mergedEvents[-1][0] - position) < EPSILON:
            mergedEvents[-1] = (mergedEvents[-1][0], mergedEvents[-1][1] + delta)
        else:
            mergedEvents.append((position, delta))

    segmentStarts = []
    segmentEnds = []
    segmentSlopes = []
    segmentValues = []

    slope = 0.0
    value = 0.0
    previous = 0.0
    for position, delta in mergedEvents:
        if position > maxSplitTotal:
            break
        if position > previous:
            segmentStarts.append(previous)
            segmentEnds.append(position)
            segmentSlopes.append(slope)
            segmentValues.append(value)
            value += slope * (position - previous)
            previous = position
        slope += delta

    if previous < maxSplitTotal:
        segmentStarts.append(previous)
        segmentEnds.append(maxSplitTotal)
        segmentSlopes.append(slope)
        segmentValues.append(value)

    return segmentStarts, segmentEnds, segmentSlopes, segmentValues


def winningMeasureAt(segmentData, splitTotal):
    segmentStarts, segmentEnds, segmentSlopes, segmentValues = segmentData
    index = bisect.bisect_right(segmentEnds, splitTotal)
    if index >= len(segmentStarts):
        return 0.0, 0.0

    start = segmentStarts[index]
    slope = segmentSlopes[index]
    value = segmentValues[index] + slope * (splitTotal - start)
    return value, slope


def expectedGain(length, segmentData):
    straightMeasure, _ = winningMeasureAt(segmentData, length - 1.0)
    diagonalMeasure, _ = winningMeasureAt(segmentData, length - SQRT_TWO)
    straightProbability = straightMeasure / (length - 1.0)
    diagonalProbability = diagonalMeasure / (length - SQRT_TWO)
    return 0.5 * length * (straightProbability + diagonalProbability)


def localDerivativeTerm(slope, intercept, squareLength, length):
    denominator = (length - squareLength) ** 2
    numerator = (
        slope * length * length
        - 2.0 * slope * squareLength * length
        - intercept * squareLength
    )
    return numerator / denominator


def optimalExpectedGain(lower, upper):
    maxLength = upper
    starts, ends, grundyValues = grundyIntervals(maxLength)
    segmentData = winningMeasureSegments(starts, ends, grundyValues, maxLength)
    segmentStarts, segmentEnds, _, _ = segmentData

    candidates = [float(lower), float(upper)]
    for point in segmentStarts + segmentEnds:
        for squareLength in (1.0, SQRT_TWO):
            length = point + squareLength
            if lower < length < upper:
                candidates.append(length)
    candidates = sorted(set(candidates))

    best = -1.0

    def consider(value):
        nonlocal best
        best = max(best, value)

    for index in range(len(candidates) - 1):
        left = candidates[index]
        right = candidates[index + 1]
        if right - left < EPSILON:
            continue

        midpoint = (left + right) / 2.0
        straightMeasure, straightSlope = winningMeasureAt(segmentData, midpoint - 1.0)
        diagonalMeasure, diagonalSlope = winningMeasureAt(segmentData, midpoint - SQRT_TWO)

        straightIntercept = straightMeasure - straightSlope * midpoint
        diagonalIntercept = diagonalMeasure - diagonalSlope * midpoint

        def valueAt(length):
            straight = (straightSlope * length + straightIntercept) / (length - 1.0)
            diagonal = (diagonalSlope * length + diagonalIntercept) / (length - SQRT_TWO)
            return 0.5 * length * (straight + diagonal)

        def derivativeAt(length):
            return 0.5 * (
                localDerivativeTerm(straightSlope, straightIntercept, 1.0, length)
                + localDerivativeTerm(diagonalSlope, diagonalIntercept, SQRT_TWO, length)
            )

        consider(valueAt(left))
        consider(valueAt(midpoint))
        consider(valueAt(right))

        rootLeft = left + 1e-10
        rootRight = right - 1e-10
        if rootLeft >= rootRight:
            continue

        samplePoints = [
            (rootLeft, derivativeAt(rootLeft)),
            (midpoint, derivativeAt(midpoint)),
            (rootRight, derivativeAt(rootRight)),
        ]
        for (a, da), (b, db) in zip(samplePoints, samplePoints[1:]):
            if da == 0.0:
                consider(valueAt(a))
            if da * db >= 0.0:
                continue

            lo = a
            hi = b
            dlo = da
            for _ in range(60):
                mid = (lo + hi) / 2.0
                dmid = derivativeAt(mid)
                if dmid == 0.0:
                    lo = hi = mid
                    break
                if dmid * dlo > 0.0:
                    lo = mid
                    dlo = dmid
                else:
                    hi = mid
            consider(valueAt((lo + hi) / 2.0))

    return f"{best:.8f}"


def runTests():
    starts, ends, grundyValues = grundyIntervals(20.0)
    segmentData = winningMeasureSegments(starts, ends, grundyValues, 20.0)
    assert f"{expectedGain(2.0, segmentData):.8f}" == "2.00000000"
    assert f"{expectedGain(4.0, segmentData):.8f}" == "1.11974851"
    assert optimalExpectedGain(2, 10) == "2.61969775"
    assert optimalExpectedGain(10, 20) == "5.99374121"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = optimalExpectedGain(200, 500)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
