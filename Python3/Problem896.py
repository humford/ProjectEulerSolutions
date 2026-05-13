from math import gcd
import time


TARGET_LENGTH = 36
TARGET_INDEX = 36


def extendedGcd(a, b):
    oldR, r = a, b
    oldS, s = 1, 0
    oldT, t = 0, 1

    while r:
        quotient = oldR // r
        oldR, r = r, oldR - quotient * r
        oldS, s = s, oldS - quotient * s
        oldT, t = t, oldT - quotient * t

    return oldR, oldS, oldT


def crtMerge(r1, m1, r2, m2):
    divisor = gcd(m1, m2)
    if (r2 - r1) % divisor:
        return None

    reducedM1 = m1 // divisor
    reducedM2 = m2 // divisor
    difference = (r2 - r1) // divisor
    _, inverse, _ = extendedGcd(reducedM1, reducedM2)
    t = difference * inverse % reducedM2
    modulus = reducedM1 * m2
    return (r1 + m1 * t) % modulus, modulus


def lcmUpTo(limit):
    value = 1

    for number in range(1, limit + 1):
        value = value // gcd(value, number) * number

    return value


def candidateOffsets(length, unusedMask, residue, step):
    offsets = []

    offset = residue
    while offset < length:
        if unusedMask & (1 << offset):
            offsets.append(offset)
        offset += step

    return offsets


def chooseMostRestricted(length, residue, modulus, unusedMask, remainingMask):
    bestIndex = None
    bestCandidates = None

    for index in range(length, 0, -1):
        if not (remainingMask & (1 << (index - 1))):
            continue

        divisor = gcd(modulus, index)
        candidates = candidateOffsets(length, unusedMask, (-residue) % divisor, divisor)
        if not candidates:
            return None
        if bestCandidates is None or len(candidates) < len(bestCandidates):
            bestIndex = index
            bestCandidates = candidates

    return bestIndex, bestCandidates


def validResidues(length):
    allOffsets = (1 << length) - 1
    allIndices = (1 << length) - 1
    residues = set()
    visited = set()

    def search(residue, modulus, unusedMask, remainingMask):
        residue %= modulus
        state = (residue, modulus, unusedMask, remainingMask)
        if state in visited:
            return
        visited.add(state)

        if remainingMask == 0:
            residues.add(residue)
            return

        choice = chooseMostRestricted(
            length,
            residue,
            modulus,
            unusedMask,
            remainingMask,
        )
        if choice is None:
            return

        index, offsets = choice
        nextRemaining = remainingMask & ~(1 << (index - 1))

        for offset in offsets:
            merged = crtMerge(residue, modulus, (-offset) % index, index)
            if merged is None:
                continue
            nextResidue, nextModulus = merged
            search(
                nextResidue,
                nextModulus,
                unusedMask & ~(1 << offset),
                nextRemaining,
            )

    search(0, 1, allOffsets, allIndices)
    return residues, lcmUpTo(length)


def nthDivisibleRangeStart(length, index):
    residues, modulus = validResidues(length)
    starts = sorted(residue if residue > 0 else modulus for residue in residues)
    return starts[index - 1]


def isDivisibleRange(start, length):
    adjacency = [
        [
            offset
            for offset in range(length)
            if (start + offset) % index == 0
        ]
        for index in range(1, length + 1)
    ]
    matchedTo = [-1] * length

    def augment(index, seen):
        for offset in adjacency[index]:
            if seen[offset]:
                continue
            seen[offset] = True
            if matchedTo[offset] == -1 or augment(matchedTo[offset], seen):
                matchedTo[offset] = index
                return True
        return False

    order = sorted(range(length), key=lambda index: len(adjacency[index]))
    for index in order:
        if not augment(index, [False] * length):
            return False

    return True


def solve():
    return nthDivisibleRangeStart(TARGET_LENGTH, TARGET_INDEX)


def runTests():
    assert nthDivisibleRangeStart(4, 1) == 1
    assert nthDivisibleRangeStart(4, 2) == 2
    assert nthDivisibleRangeStart(4, 3) == 3
    assert nthDivisibleRangeStart(4, 4) == 6
    assert isDivisibleRange(6, 4)
    assert isDivisibleRange(274229635640, 36)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
