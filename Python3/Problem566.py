import os
import time
from bisect import bisect_right
from concurrent.futures import ProcessPoolExecutor
from math import isqrt, lcm, sqrt


EPSILON = 1e-11
POINT_SCALE = 10 ** 12


def endpointKey(value):
    value %= 1.0
    if value < EPSILON or 1.0 - value < EPSILON:
        return 0
    return int(round(value * POINT_SCALE)) % POINT_SCALE


def flipNegativeIntervals(negativeIntervals, angle, nextAngle):
    affected = []
    unaffected = []

    for lower, upper in negativeIntervals:
        if lower >= angle - EPSILON:
            unaffected.append((lower, upper))
        elif upper > angle + EPSILON:
            affected.append((lower, angle))
            unaffected.append((angle, upper))
        else:
            affected.append((lower, upper))

    positiveInSlice = [(angle - upper, angle - lower) for lower, upper in affected]
    positiveInSlice.sort()

    nextIntervals = list(unaffected)
    cursor = 0.0
    for lower, upper in positiveInSlice:
        if lower - cursor > EPSILON:
            nextIntervals.append((cursor, lower))
        if upper > cursor:
            cursor = upper
    if angle - cursor > EPSILON:
        nextIntervals.append((cursor, angle))

    rotated = []
    for lower, upper in nextIntervals:
        lower += nextAngle
        upper += nextAngle
        if upper <= 1.0 + EPSILON:
            rotated.append((lower, min(upper, 1.0)))
        elif lower >= 1.0 - EPSILON:
            rotated.append((lower - 1.0, upper - 1.0))
        else:
            rotated.append((lower, 1.0))
            rotated.append((0.0, upper - 1.0))

    rotated.sort()
    merged = []
    for lower, upper in rotated:
        if upper - lower <= EPSILON:
            continue
        if merged and abs(merged[-1][1] - lower) < EPSILON:
            merged[-1] = (merged[-1][0], upper)
        else:
            merged.append((lower, upper))
    return merged


def discoverEndpoints(a, b, c, quietLimit=5_000, maxSteps=300_000):
    angles = (1 / a, 1 / b, 1 / sqrt(c))
    endpointKeys = {0}
    negativeIntervals = []
    quietSteps = 0

    for step in range(maxSteps):
        before = len(endpointKeys)
        angle = angles[step % 3]
        endpointKeys.add(endpointKey(angle))
        negativeIntervals = flipNegativeIntervals(
            negativeIntervals, angle, angles[(step + 1) % 3]
        )
        for lower, upper in negativeIntervals:
            endpointKeys.add(endpointKey(lower))
            endpointKeys.add(endpointKey(upper))

        if len(endpointKeys) == before:
            quietSteps += 1
        else:
            quietSteps = 0
        if quietSteps >= quietLimit:
            break
    else:
        raise RuntimeError(f"Endpoint discovery did not stabilize for {(a, b, c)}")

    return sorted(key / POINT_SCALE for key in endpointKeys), angles


def atomIndex(endpoints, value):
    value %= 1.0
    if value < EPSILON or 1.0 - value < EPSILON:
        value = 0.0
    index = bisect_right(endpoints, value) - 1
    return index if index >= 0 else len(endpoints) - 1


def buildStepMap(endpoints, angles, phase):
    angle = angles[phase]
    nextAngle = angles[(phase + 1) % 3]
    source = []
    toggle = []

    for index, lower in enumerate(endpoints):
        upper = endpoints[index + 1] if index + 1 < len(endpoints) else 1.0
        targetMidpoint = (lower + upper) / 2
        beforeRotation = (targetMidpoint - nextAngle) % 1.0

        if beforeRotation <= angle + EPSILON:
            source.append(atomIndex(endpoints, angle - beforeRotation))
            toggle.append(1)
        else:
            source.append(atomIndex(endpoints, beforeRotation))
            toggle.append(0)
    return source, toggle


def composeMaps(first, second):
    firstSource, firstToggle = first
    secondSource, secondToggle = second
    return (
        [firstSource[secondSource[index]] for index in range(len(secondSource))],
        [
            firstToggle[secondSource[index]] ^ secondToggle[index]
            for index in range(len(secondSource))
        ],
    )


def componentCongruenceClasses(source, toggle, constraints):
    graph = [[] for _ in source]
    for index, nextIndex in enumerate(source):
        graph[index].append(nextIndex)
        graph[nextIndex].append(index)

    seen = [False] * len(source)
    classes = []
    for start in range(len(source)):
        if seen[start]:
            continue

        stack = [start]
        seen[start] = True
        nodes = []
        while stack:
            node = stack.pop()
            nodes.append(node)
            for neighbor in graph[node]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    stack.append(neighbor)

        componentConstraints = {
            node: constraints[node] for node in nodes if node in constraints
        }
        if not componentConstraints:
            continue

        pathIndex = {}
        path = []
        node = start
        while node not in pathIndex:
            pathIndex[node] = len(path)
            path.append(node)
            node = source[node]

        cycle = path[pathIndex[node] :]
        cycleParity = 0
        for cycleNode in cycle:
            cycleParity ^= toggle[cycleNode]
        period = len(cycle) * (2 if cycleParity else 1)

        values = {node: 0 for node in componentConstraints}
        allowed = []
        for residue in range(period):
            if all(
                values[node] == desired
                for node, desired in componentConstraints.items()
            ):
                allowed.append(residue)
            previous = values
            values = {
                node: previous[source[node]] ^ toggle[node] for node in previous
            }

        classes.append((period, allowed))
    return classes


def combineCongruences(classes, minimumValue):
    residues = {0}
    modulus = 1

    for period, allowedResidues in classes:
        allowedResidues = set(allowedResidues)
        nextModulus = lcm(modulus, period)
        nextResidues = set()
        for residue in residues:
            for candidate in range(residue, nextModulus, modulus):
                if candidate % period in allowedResidues:
                    nextResidues.add(candidate)
        residues = nextResidues
        modulus = nextModulus
        if not residues:
            return None

    best = None
    for residue in residues:
        candidate = residue
        if candidate < minimumValue:
            candidate += ((minimumValue - candidate + modulus - 1) // modulus) * modulus
        if best is None or candidate < best:
            best = candidate
    return best


def firstConstrainedBlockTime(blockMap, constraints, minimumValue):
    source, toggle = blockMap
    classes = componentCongruenceClasses(source, toggle, constraints)
    return combineCongruences(classes, minimumValue)


def stepPartitionFlips(a, b, c):
    endpoints, angles = discoverEndpoints(a, b, c)
    atomCount = len(endpoints)
    stepMaps = [buildStepMap(endpoints, angles, phase) for phase in range(3)]

    identity = (list(range(atomCount)), [0] * atomCount)
    remainderMaps = [
        identity,
        stepMaps[0],
        composeMaps(stepMaps[0], stepMaps[1]),
    ]
    blockMap = composeMaps(composeMaps(stepMaps[0], stepMaps[1]), stepMaps[2])

    best = None
    for remainder, remainderMap in enumerate(remainderMaps):
        source, toggle = remainderMap
        constraints = {}
        valid = True
        for index, sourceIndex in enumerate(source):
            desired = toggle[index]
            if sourceIndex in constraints and constraints[sourceIndex] != desired:
                valid = False
                break
            constraints[sourceIndex] = desired
        if not valid:
            continue

        blockCount = firstConstrainedBlockTime(
            blockMap, constraints, 1 if remainder == 0 else 0
        )
        if blockCount is None:
            continue
        candidate = 3 * blockCount + remainder
        if candidate > 0 and (best is None or candidate < best):
            best = candidate

    if best is None:
        raise RuntimeError(f"No return time found for {(a, b, c)}")
    return best


def isSquare(n):
    root = isqrt(n)
    return root * root == n


def blockCutPairs(a, b):
    denominator = lcm(a, b)
    aStep = denominator // a
    bStep = denominator // b
    return denominator, aStep, bStep


def pairValue(pair, denominator, root):
    rationalPart, radicalPart = pair
    return (rationalPart / denominator + radicalPart / root) % 1.0


def blockCutIndex(pair, denominator, aStep, bStep):
    cuts = {
        (0, 0): 0,
        (aStep, 0): 1,
        ((-bStep) % denominator, -1): 2,
        ((-bStep) % denominator, 0): 3,
    }
    return cuts.get(pair)


def blockBranchForPair(pair, side, a, b, c, denominator, aStep, bStep, root):
    cutIndex = blockCutIndex(pair, denominator, aStep, bStep)
    if cutIndex is not None:
        leftBranches = (3, 0, 1, 2)
        rightBranches = (0, 1, 2, 3)
        return leftBranches[cutIndex] if side == "L" else rightBranches[cutIndex]

    value = pairValue(pair, denominator, root)
    if value < 1 / a:
        return 0
    if value < 1 - 1 / b - 1 / root:
        return 1
    if value < 1 - 1 / b:
        return 2
    return 3


def stepBlockSideState(state, a, b, c, denominator, aStep, bStep, root):
    pair, side = state
    rationalPart, radicalPart = pair
    branch = blockBranchForPair(
        pair, side, a, b, c, denominator, aStep, bStep, root
    )

    if branch == 0:
        nextPair = ((2 * aStep + bStep - rationalPart) % denominator, 1 - radicalPart)
        slope = -1
    elif branch == 1:
        nextPair = ((rationalPart + aStep + bStep) % denominator, radicalPart + 1)
        slope = 1
    elif branch == 2:
        nextPair = ((aStep - bStep - rationalPart) % denominator, -radicalPart)
        slope = -1
    else:
        nextPair = ((aStep - rationalPart) % denominator, 1 - radicalPart)
        slope = -1

    if slope == -1:
        side = "L" if side == "R" else "R"
    return nextPair, side


def collectBlockEndpoints(a, b, c, orbitLimit=10_000_000):
    denominator, aStep, bStep = blockCutPairs(a, b)
    root = sqrt(c)
    cuts = [
        (0, 0),
        (aStep, 0),
        ((-bStep) % denominator, -1),
        ((-bStep) % denominator, 0),
    ]
    endpoints = set(cuts)

    for cut in cuts:
        for side in ("L", "R"):
            state = (cut, side)
            seen = set()
            for _ in range(orbitLimit):
                if state in seen:
                    break
                seen.add(state)
                endpoints.add(state[0])
                state = stepBlockSideState(
                    state, a, b, c, denominator, aStep, bStep, root
                )
            else:
                raise RuntimeError(f"Block endpoint orbit did not close for {(a, b, c)}")

    return denominator, root, endpoints


def blockImage(value, a, b, root):
    x = 1 / a
    y = 1 / b
    z = 1 / root

    if value < x:
        return (2 * x + y + z - value) % 1.0, 1
    if value < 1 - y - z:
        return (value + x + y + z) % 1.0, 0
    if value < 1 - y:
        return (1 + x - y - value) % 1.0, 1
    return (1 + x + z - value) % 1.0, 1


def minimalSequencePeriod(sequence):
    prefix = [0] * len(sequence)
    for index in range(1, len(sequence)):
        candidate = prefix[index - 1]
        while candidate and sequence[index] != sequence[candidate]:
            candidate = prefix[candidate - 1]
        if sequence[index] == sequence[candidate]:
            candidate += 1
        prefix[index] = candidate

    period = len(sequence) - prefix[-1]
    if len(sequence) % period == 0:
        return period
    return len(sequence)


def cycleOrientationPeriod(toggles):
    parityPrefix = [0]
    for toggle in toggles:
        parityPrefix.append(parityPrefix[-1] ^ toggle)

    cycleParity = parityPrefix[-1]
    sequence = parityPrefix[:-1]
    if cycleParity:
        sequence = sequence + [value ^ 1 for value in sequence]
    return minimalSequencePeriod(sequence)


def blockPartitionFlips(a, b, c):
    denominator, root, endpointPairs = collectBlockEndpoints(a, b, c)
    endpoints = sorted(pairValue(pair, denominator, root) for pair in endpointPairs)
    atomCount = len(endpoints)

    forward = [0] * atomCount
    toggles = [0] * atomCount
    for index, lower in enumerate(endpoints):
        upper = endpoints[index + 1] if index + 1 < atomCount else endpoints[0] + 1.0
        midpoint = ((lower + upper) / 2) % 1.0
        image, toggle = blockImage(midpoint, a, b, root)
        target = bisect_right(endpoints, image) - 1
        if target < 0:
            target = atomCount - 1
        forward[index] = target
        toggles[index] = toggle

    indegrees = [0] * atomCount
    for target in forward:
        indegrees[target] += 1
    if any(indegree != 1 for indegree in indegrees):
        raise RuntimeError(f"Block atom map is not a permutation for {(a, b, c)}")

    blockCount = 1
    seen = [False] * atomCount
    for start in range(atomCount):
        if seen[start]:
            continue
        atom = start
        cycleToggles = []
        while not seen[atom]:
            seen[atom] = True
            cycleToggles.append(toggles[atom])
            atom = forward[atom]
        blockCount = lcm(blockCount, cycleOrientationPeriod(cycleToggles))

    return 3 * blockCount


def flips(a, b, c):
    if isSquare(c):
        return stepPartitionFlips(a, b, c)
    return blockPartitionFlips(a, b, c)


def tupleFlips(triple):
    return flips(*triple)


def triplesUpTo(n):
    for a in range(9, n - 1):
        for b in range(a + 1, n):
            for c in range(b + 1, n + 1):
                yield (a, b, c)


def cakeIcingSum(n, workers=1):
    triples = list(triplesUpTo(n))
    if n <= 17:
        return sum(tupleFlips(triple) for triple in triples)

    if workers is None:
        workers = min(8, os.cpu_count() or 1)
    if workers <= 1:
        return sum(tupleFlips(triple) for triple in triples)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        return sum(executor.map(tupleFlips, triples, chunksize=8))


def runTests():
    assert flips(9, 10, 11) == 60
    assert flips(10, 14, 16) == 506
    assert flips(15, 16, 17) == 785_232
    assert cakeIcingSum(11) == 60
    assert cakeIcingSum(14) == 58_020
    assert cakeIcingSum(17) == 1_269_260


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = cakeIcingSum(53)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
