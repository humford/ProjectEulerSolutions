from collections import deque
import time


MODULUS = 1_000_000_007


def precomputeFactorials(limit):
    factorial = [1] * (limit + 1)
    inverseFactorial = [1] * (limit + 1)

    for i in range(1, limit + 1):
        factorial[i] = factorial[i - 1] * i % MODULUS

    inverseFactorial[limit] = pow(factorial[limit], MODULUS - 2, MODULUS)
    for i in range(limit, 0, -1):
        inverseFactorial[i - 1] = inverseFactorial[i] * i % MODULUS

    return factorial, inverseFactorial


def chooseSmall(n, k, inverseFactorial):
    if k < 0 or n < k:
        return 0
    if k == 0:
        return 1

    numerator = 1
    for i in range(k):
        numerator = numerator * ((n - i) % MODULUS) % MODULUS

    return numerator * inverseFactorial[k] % MODULUS


def nfaNext(a, b, pairUsed, tileCount):
    if a + b > tileCount:
        return ()

    remaining = tileCount - a - b
    pairChoices = (0, 1) if pairUsed == 0 else (0,)
    states = []

    for pair in pairChoices:
        if 2 * pair > remaining:
            continue
        afterPair = remaining - 2 * pair

        for pung in (0, 1):
            if 3 * pung > afterPair:
                continue

            newChows = afterPair - 3 * pung
            if newChows <= 4:
                states.append((newChows, a, pairUsed | pair))

    if len(states) <= 1:
        return tuple(states)
    return tuple(sorted(set(states)))


def buildDfa():
    nfaStates = [(a, b, pairUsed) for a in range(5) for b in range(5) for pairUsed in (0, 1)]
    nfaIndex = {state: i for i, state in enumerate(nfaStates)}
    nfaTransitions = [[()] * 5 for _ in range(len(nfaStates))]

    for state in nfaStates:
        stateIndex = nfaIndex[state]
        a, b, pairUsed = state
        for tileCount in range(5):
            nextStates = nfaNext(a, b, pairUsed, tileCount)
            nfaTransitions[stateIndex][tileCount] = tuple(nfaIndex[nextState] for nextState in nextStates)

    initial = frozenset([nfaIndex[(0, 0, 0)]])
    queue = deque([initial])
    dfaIndex = {initial: 0}
    dfaStates = []
    dfaTransitions = []

    while queue:
        stateSet = queue.popleft()
        dfaStates.append(stateSet)
        row = []

        for tileCount in range(5):
            nextSet = set()
            for stateIndex in stateSet:
                nextSet.update(nfaTransitions[stateIndex][tileCount])

            frozenNextSet = frozenset(nextSet)
            if frozenNextSet not in dfaIndex:
                dfaIndex[frozenNextSet] = len(dfaIndex)
                queue.append(frozenNextSet)
            row.append(dfaIndex[frozenNextSet])

        dfaTransitions.append(row)

    zeroTransitions = [dfaTransitions[i][0] for i in range(len(dfaStates))]
    boundaryNoPair = dfaIndex[frozenset([nfaIndex[(0, 0, 0)]])]
    boundaryPair = dfaIndex[frozenset([nfaIndex[(0, 0, 1)]])]

    return dfaStates, dfaTransitions, zeroTransitions, boundaryNoPair, boundaryPair


DFA_STATES, DFA_TRANSITIONS, ZERO_TRANSITIONS, BOUNDARY_NO_PAIR, BOUNDARY_PAIR = buildDfa()


def buildBlockTables(maxLength, maxTiles):
    stateCount = len(DFA_STATES)
    counts = [[0] * (maxTiles + 1) for _ in range(stateCount)]
    counts[BOUNDARY_NO_PAIR][0] = 1

    noPairBlocks = [[0] * (maxTiles + 1) for _ in range(maxLength + 1)]
    pairBlocks = [[0] * (maxTiles + 1) for _ in range(maxLength + 1)]

    for length in range(1, maxLength + 1):
        nextCounts = [[0] * (maxTiles + 1) for _ in range(stateCount)]

        for state in range(stateCount):
            row = counts[state]
            for tileCount in range(1, 5):
                nextState = DFA_TRANSITIONS[state][tileCount]
                nextRow = nextCounts[nextState]
                for tiles in range(maxTiles - tileCount + 1):
                    value = row[tiles]
                    if value:
                        nextRow[tiles + tileCount] = (nextRow[tiles + tileCount] + value) % MODULUS

        counts = nextCounts

        for state in range(stateCount):
            boundaryState = ZERO_TRANSITIONS[state]
            if boundaryState == BOUNDARY_NO_PAIR:
                target = noPairBlocks[length]
            elif boundaryState == BOUNDARY_PAIR:
                target = pairBlocks[length]
            else:
                continue

            for tiles, value in enumerate(counts[state]):
                if value:
                    target[tiles] = (target[tiles] + value) % MODULUS

    noPairTerms = [[] for _ in range(maxLength + 1)]
    pairTerms = [[] for _ in range(maxLength + 1)]
    for length in range(1, maxLength + 1):
        for tiles in range(maxTiles + 1):
            value = noPairBlocks[length][tiles]
            if value:
                noPairTerms[length].append((tiles, value))
            value = pairBlocks[length][tiles]
            if value:
                pairTerms[length].append((tiles, value))

    return noPairTerms, pairTerms


def convolveLengthTilePolynomial(left, rightTerms, maxLength, maxTiles):
    result = [[0] * (maxTiles + 1) for _ in range(maxLength + 1)]

    for leftLength in range(maxLength + 1):
        leftRow = left[leftLength]
        if not any(leftRow):
            continue

        for rightLength in range(1, maxLength - leftLength + 1):
            terms = rightTerms[rightLength]
            if not terms:
                continue

            resultRow = result[leftLength + rightLength]
            for leftTiles, leftValue in enumerate(leftRow):
                if not leftValue:
                    continue

                for rightTiles, rightValue in terms:
                    tileTotal = leftTiles + rightTiles
                    if tileTotal <= maxTiles:
                        resultRow[tileTotal] = (resultRow[tileTotal] + leftValue * rightValue) % MODULUS

    return result


def perSuitPolynomials(tileCount, triples):
    maxTiles = 3 * triples + 2
    maxLength = min(maxTiles, tileCount)
    noPairTerms, pairTerms = buildBlockTables(maxLength, maxTiles)
    _, inverseFactorial = precomputeFactorials(maxLength)

    noPairPower = [[0] * (maxTiles + 1) for _ in range(maxLength + 1)]
    noPairPower[0][0] = 1
    noPairByTiles = [0] * (maxTiles + 1)
    pairByTiles = [0] * (maxTiles + 1)

    for noPairBlockCount in range(maxLength + 1):
        for positiveLength in range(maxLength + 1):
            placementChoices = chooseSmall(tileCount - positiveLength + 1, noPairBlockCount, inverseFactorial)
            if not placementChoices:
                continue

            row = noPairPower[positiveLength]
            for tiles, value in enumerate(row):
                if value:
                    noPairByTiles[tiles] = (noPairByTiles[tiles] + value * placementChoices) % MODULUS

        totalBlockCount = noPairBlockCount + 1
        if totalBlockCount <= maxLength:
            withPair = convolveLengthTilePolynomial(noPairPower, pairTerms, maxLength, maxTiles)
            for positiveLength in range(maxLength + 1):
                placementChoices = chooseSmall(tileCount - positiveLength + 1, totalBlockCount, inverseFactorial)
                if not placementChoices:
                    continue

                factor = placementChoices * totalBlockCount % MODULUS
                row = withPair[positiveLength]
                for tiles, value in enumerate(row):
                    if value:
                        pairByTiles[tiles] = (pairByTiles[tiles] + value * factor) % MODULUS

        if noPairBlockCount != maxLength:
            noPairPower = convolveLengthTilePolynomial(noPairPower, noPairTerms, maxLength, maxTiles)

    noPairPolynomial = [0] * (triples + 1)
    pairPolynomial = [0] * (triples + 1)
    for k in range(triples + 1):
        noPairPolynomial[k] = noPairByTiles[3 * k]
        pairPolynomial[k] = pairByTiles[3 * k + 2]

    return noPairPolynomial, pairPolynomial


def multiplyPolynomials(left, right, degree):
    result = [0] * (degree + 1)

    for i, leftValue in enumerate(left):
        if not leftValue:
            continue

        for j, rightValue in enumerate(right):
            if not rightValue:
                continue
            if i + j > degree:
                break
            result[i + j] = (result[i + j] + leftValue * rightValue) % MODULUS

    return result


def powerPolynomial(polynomial, exponent, degree):
    result = [0] * (degree + 1)
    result[0] = 1
    base = polynomial[:]

    while exponent:
        if exponent & 1:
            result = multiplyPolynomials(result, base, degree)
        exponent >>= 1
        if exponent:
            base = multiplyPolynomials(base, base, degree)

    return result


def winningHandCount(tileCount, suits, triples):
    noPairPolynomial, pairPolynomial = perSuitPolynomials(tileCount, triples)
    otherSuits = powerPolynomial(noPairPolynomial, suits - 1, triples)

    total = 0
    for k in range(triples + 1):
        total = (total + pairPolynomial[k] * otherSuits[triples - k]) % MODULUS

    return total * (suits % MODULUS) % MODULUS


def runTests():
    assert winningHandCount(4, 1, 1) == 20
    assert winningHandCount(9, 1, 4) == 13_259
    assert winningHandCount(9, 3, 4) == 5_237_550
    assert winningHandCount(1_000, 1_000, 5) == 107_662_178


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningHandCount(10 ** 8, 10 ** 8, 30)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
