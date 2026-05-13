from decimal import Decimal, ROUND_HALF_UP, getcontext
import time


def maximumComponentExpectationRational(width, height):
    cells = width * height
    startLabels = (0,) * width
    startSizes = ()
    states = {(startLabels, startSizes): {0: 1}}
    transitionCache = {}

    for index in range(cells):
        column = index % width
        nextStates = {}

        for (labels, sizes), maximumCounts in states.items():
            leftId = labels[column - 1] if column else 0
            upId = labels[column]

            for colour in (0, 1):
                key = (labels, sizes, column, colour)
                transition = transitionCache.get(key)

                if transition is None:
                    nextLabels = list(labels)
                    nextSizes = list(sizes)

                    if colour == 0:
                        nextLabels[column] = 0
                    elif leftId == 0 and upId == 0:
                        nextSizes.append(1)
                        nextLabels[column] = len(nextSizes)
                    elif upId == 0:
                        nextSizes[leftId - 1] += 1
                        nextLabels[column] = leftId
                    elif leftId == 0:
                        nextSizes[upId - 1] += 1
                        nextLabels[column] = upId
                    elif leftId == upId:
                        nextSizes[leftId - 1] += 1
                        nextLabels[column] = leftId
                    else:
                        nextSizes[leftId - 1] += nextSizes[upId - 1] + 1
                        nextSizes[upId - 1] = 0
                        for j in range(width):
                            if nextLabels[j] == upId:
                                nextLabels[j] = leftId
                        nextLabels[column] = leftId

                    present = [False] * (len(nextSizes) + 1)
                    for label in nextLabels:
                        if label:
                            present[label] = True

                    closedMaximum = 0
                    for componentId in range(1, len(nextSizes) + 1):
                        size = nextSizes[componentId - 1]
                        if size and not present[componentId]:
                            closedMaximum = max(closedMaximum, size)
                            nextSizes[componentId - 1] = 0

                    mapping = [0] * (len(nextSizes) + 1)
                    canonicalLabels = [0] * width
                    canonicalSizes = []
                    nextId = 0

                    for j, label in enumerate(nextLabels):
                        if label == 0:
                            continue

                        mapped = mapping[label]
                        if mapped == 0:
                            nextId += 1
                            mapped = nextId
                            mapping[label] = mapped
                            canonicalSizes.append(nextSizes[label - 1])
                        canonicalLabels[j] = mapped

                    transition = (tuple(canonicalLabels), tuple(canonicalSizes), closedMaximum)
                    transitionCache[key] = transition

                nextLabels, nextSizes, closedMaximum = transition
                stateKey = (nextLabels, nextSizes)
                target = nextStates.setdefault(stateKey, {})

                if closedMaximum == 0:
                    for maximum, count in maximumCounts.items():
                        target[maximum] = target.get(maximum, 0) + count
                else:
                    for maximum, count in maximumCounts.items():
                        updatedMaximum = max(maximum, closedMaximum)
                        target[updatedMaximum] = target.get(updatedMaximum, 0) + count

        states = nextStates

    denominator = 1 << cells
    numerator = 0

    for (_labels, sizes), maximumCounts in states.items():
        activeMaximum = max(sizes) if sizes else 0
        for maximum, count in maximumCounts.items():
            numerator += max(maximum, activeMaximum) * count

    return numerator, denominator


def expectedConnectedArea(width, height, places=8):
    numerator, denominator = maximumComponentExpectationRational(width, height)
    getcontext().prec = 80
    value = Decimal(numerator) / Decimal(denominator)
    quantum = Decimal("1." + "0" * places)
    return str(value.quantize(quantum, rounding=ROUND_HALF_UP))


def runTests():
    numerator, denominator = maximumComponentExpectationRational(2, 2)
    assert (numerator, denominator) == (30, 16)
    assert expectedConnectedArea(2, 2, 3) == "1.875"
    assert expectedConnectedArea(4, 4) == "5.76487732"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedConnectedArea(7, 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
