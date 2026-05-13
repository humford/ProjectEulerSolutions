import time


MOD = 1_000_000_000


def popcount4(mask):
    return mask.bit_count()


def expandShotVector(vector):
    a0, a1, a2, a3 = vector
    return (a0 + a3, a1 + a0, a2 + a1, a3 + a2)


def buildStates():
    states = []
    indexByState = {}
    for a0 in range(4):
        for a1 in range(4 - a0):
            for a2 in range(4 - a0 - a1):
                for a3 in range(4 - a0 - a1 - a2):
                    state = (a0, a1, a2, a3)
                    indexByState[state] = len(states)
                    states.append(state)
    return states, indexByState


def buildTransitions(states, indexByState):
    terminal = indexByState[(0, 0, 0, 0)]
    popcounts = [popcount4(mask) for mask in range(16)]
    nonterminalTransitions = [[] for _ in states]
    terminalWeights = [[] for _ in states]

    for stateIndex, state in enumerate(states):
        if stateIndex == terminal:
            continue

        expanded = expandShotVector(state)
        for mask in range(16):
            nextState = (
                expanded[0] - (mask & 1),
                expanded[1] - ((mask >> 1) & 1),
                expanded[2] - ((mask >> 2) & 1),
                expanded[3] - ((mask >> 3) & 1),
            )
            if min(nextState) < 0 or max(nextState) > 3 or sum(nextState) > 3:
                continue

            nextIndex = indexByState.get(nextState)
            if nextIndex is None:
                continue

            weight = popcounts[mask]
            if nextIndex == terminal:
                terminalWeights[stateIndex].append(weight)
            else:
                nonterminalTransitions[stateIndex].append((nextIndex, weight))

    return terminal, nonterminalTransitions, terminalWeights


def computeAll(maxDivisions, mod=MOD):
    states, indexByState = buildStates()
    terminal, nonterminalTransitions, terminalWeights = buildTransitions(states, indexByState)
    order = sorted(range(len(states)), key=lambda i: (sum(states[i]), states[i]))
    start = indexByState[(1, 0, 0, 0)]
    maxAmoebas = maxDivisions + 1

    finishedByAmoebas = [0] * (maxAmoebas + 1)
    layers = [[0] * len(states) for _ in range(5)]
    layers[0][start] = 1

    for amoebas in range(maxAmoebas + 1):
        current = layers[0]
        for stateIndex in order:
            value = current[stateIndex]
            if value == 0:
                continue

            for weight in terminalWeights[stateIndex]:
                nextAmoebas = amoebas + weight
                if nextAmoebas <= maxAmoebas:
                    finishedByAmoebas[nextAmoebas] = (
                        finishedByAmoebas[nextAmoebas] + value
                    ) % mod

            for nextIndex, weight in nonterminalTransitions[stateIndex]:
                nextAmoebas = amoebas + weight
                if nextAmoebas > maxAmoebas:
                    continue
                if weight == 0:
                    current[nextIndex] = (current[nextIndex] + value) % mod
                else:
                    layers[weight][nextIndex] = (layers[weight][nextIndex] + value) % mod

        layers.pop(0)
        layers.append([0] * len(states))

    counts = [0] * (maxDivisions + 1)
    counts[0] = 1
    for divisions in range(1, maxDivisions + 1):
        counts[divisions] = finishedByAmoebas[divisions + 1] % mod
    return counts


def bruteCounts(maxDivisions):
    arrangements = {frozenset({(0, 0)})}
    counts = [1]
    for _ in range(maxDivisions):
        nextArrangements = set()
        for arrangement in arrangements:
            occupied = set(arrangement)
            for x, y in arrangement:
                childA = (x + 1, y)
                childB = (x + 1, (y + 1) % 4)
                if childA in occupied or childB in occupied:
                    continue
                newArrangement = set(occupied)
                newArrangement.remove((x, y))
                newArrangement.add(childA)
                newArrangement.add(childB)
                nextArrangements.add(frozenset(newArrangement))
        arrangements = nextArrangements
        counts.append(len(arrangements))
    return counts


def runTests():
    small = computeAll(20)
    assert small[:8] == bruteCounts(7)
    assert small[2] == 2
    assert small[10] == 1_301
    assert small[20] == 5_895_236
    assert computeAll(100)[100] == 125_923_036


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = computeAll(100_000)[100_000]
    elapsed = time.time() - start

    print("Found " + f"{answer:09d}" + " in " + str(elapsed) + " seconds.")
