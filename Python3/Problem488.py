import functools
import time


MODULUS = 10 ** 9


@functools.lru_cache(None)
def _is_winning(state):
    heaps = list(state)
    for index, heap in enumerate(heaps):
        for reduced in range(heap):
            next_heaps = heaps[:]
            next_heaps[index] = reduced
            if len(set(next_heaps)) < 3:
                continue
            if not _is_winning(tuple(sorted(next_heaps))):
                return True
    return False


def _boundedXorTripleCountAndSum(maxA, maxB, maxC):
    if maxA < 0 or maxB < 0 or maxC < 0:
        return 0, 0

    bitCount = max(maxA, maxB, maxC).bit_length()
    counts = [0] * 8
    sumsA = [0] * 8
    sumsB = [0] * 8
    sumsC = [0] * 8
    counts[7] = 1

    for bitIndex in range(bitCount - 1, -1, -1):
        limitA = (maxA >> bitIndex) & 1
        limitB = (maxB >> bitIndex) & 1
        limitC = (maxC >> bitIndex) & 1
        bitValue = 1 << bitIndex

        nextCounts = [0] * 8
        nextSumsA = [0] * 8
        nextSumsB = [0] * 8
        nextSumsC = [0] * 8

        for state in range(8):
            count = counts[state]
            if count == 0:
                continue

            tightA = (state >> 2) & 1
            tightB = (state >> 1) & 1
            tightC = state & 1

            for bitA in (0, 1):
                if tightA and bitA > limitA:
                    continue
                nextTightA = int(tightA and bitA == limitA)

                for bitB in (0, 1):
                    if tightB and bitB > limitB:
                        continue
                    nextTightB = int(tightB and bitB == limitB)

                    bitC = bitA ^ bitB
                    if tightC and bitC > limitC:
                        continue
                    nextTightC = int(tightC and bitC == limitC)
                    nextState = (nextTightA << 2) | (nextTightB << 1) | nextTightC

                    nextCounts[nextState] += count
                    nextSumsA[nextState] += sumsA[state] + count * bitA * bitValue
                    nextSumsB[nextState] += sumsB[state] + count * bitB * bitValue
                    nextSumsC[nextState] += sumsC[state] + count * bitC * bitValue

        counts = nextCounts
        sumsA = nextSumsA
        sumsB = nextSumsB
        sumsC = nextSumsC

    return sum(counts), sum(sumsA) + sum(sumsB) + sum(sumsC)


@functools.lru_cache(None)
def boundedXorTripleCountAndSum(maxA, maxB, maxC):
    return _boundedXorTripleCountAndSum(maxA, maxB, maxC)


def unbalancedNimSum(limit):
    orderedCount = 0
    orderedShiftedSum = 0

    for mask in range(8):
        maxA = 1 if mask & 1 else limit
        maxB = 1 if mask & 2 else limit
        maxC = 1 if mask & 4 else limit
        count, shiftedSum = boundedXorTripleCountAndSum(maxA, maxB, maxC)

        if mask.bit_count() % 2:
            orderedCount -= count
            orderedShiftedSum -= shiftedSum
        else:
            orderedCount += count
            orderedShiftedSum += shiftedSum

    return (orderedShiftedSum - 3 * orderedCount) // 6


def bruteUnbalancedNimSum(limit):
    total = 0
    for a in range(1, limit):
        for b in range(a + 1, limit):
            for c in range(b + 1, limit):
                if not _is_winning((a, b, c)):
                    total += a + b + c
    return total


def runTests():
    assert not _is_winning((2, 4, 5))
    assert unbalancedNimSum(8) == bruteUnbalancedNimSum(8)
    assert unbalancedNimSum(8) == 42
    assert unbalancedNimSum(128) == 496_062


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = unbalancedNimSum(10 ** 18) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
