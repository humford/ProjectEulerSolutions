from functools import lru_cache
import time


TARGET_EXPONENT = 13

WEIGHTS = [1, 3, 2, 6, 4, 5]
RESIDUE_MASK = 0x7F
CLASS_BITS = 0x1FF
SHIFT = [9 * index for index in range(6)]


def buildRotationTable():
    table = [[0] * 128 for _ in range(7)]
    for shift in range(7):
        for mask in range(128):
            if shift == 0:
                table[shift][mask] = mask
            else:
                table[shift][mask] = (
                    (mask << shift) | (mask >> (7 - shift))
                ) & RESIDUE_MASK
    return table


ROTATE = buildRotationTable()


def buildForbiddenShifts():
    shifts = [[[0] * 6 for _ in range(6)] for __ in range(7)]
    for residue in range(1, 7):
        for previousClass in range(6):
            for currentClass in range(6):
                if previousClass != currentClass:
                    difference = (WEIGHTS[currentClass] - WEIGHTS[previousClass]) % 7
                    shifts[residue][previousClass][currentClass] = (
                        residue * pow(difference, -1, 7)
                    ) % 7
    return shifts


FORBIDDEN_SHIFT = buildForbiddenShifts()


def buildClassMasks():
    allDigits = [0] * 512
    noLeadingZeroSwap = [0] * 512
    for bits in range(512):
        residueMask = bits & RESIDUE_MASK
        hasSeven = (bits >> 8) & 1
        allDigits[bits] = residueMask
        noZero = residueMask & ~1
        if hasSeven:
            noZero |= 1
        noLeadingZeroSwap[bits] = noZero
    return allDigits, noLeadingZeroSwap


MASK_ALL, MASK_NO_ZERO = buildClassMasks()


DIGIT_CLASSES = [
    (0, 1, 0),  # digit 0
    (0, 0, 1),  # digit 7
    (1, 0, 0),  # digits 1, 8
    (2, 0, 0),  # digits 2, 9
    (3, 0, 0),
    (4, 0, 0),
    (5, 0, 0),
    (6, 0, 0),
]
CLASS_RESIDUE = [entry[0] for entry in DIGIT_CLASSES]
CLASS_MULTIPLICITY = [1, 1, 2, 2, 1, 1, 1, 1]


def buildUpdateTable():
    table = [[0] * 8 for _ in range(512)]
    for oldBits in range(512):
        residueMask = oldBits & RESIDUE_MASK
        hasZero = (oldBits >> 7) & 1
        hasSeven = (oldBits >> 8) & 1
        for index, (residue, addsZero, addsSeven) in enumerate(DIGIT_CLASSES):
            newMask = residueMask | (1 << residue)
            newHasZero = hasZero | addsZero
            newHasSeven = hasSeven | addsSeven
            table[oldBits][index] = newMask | (newHasZero << 7) | (newHasSeven << 8)
    return table


UPDATE_CLASS = buildUpdateTable()
ADD_CONTRIBUTION = [
    [(CLASS_RESIDUE[index] * WEIGHTS[weightClass]) % 7 for index in range(8)]
    for weightClass in range(6)
]
PERMUTATION = [[(index + add) % 7 for index in range(7)] for add in range(7)]


def advance(states, position, targetResidue, isMostSignificant):
    weightClass = position % 6
    shift = SHIFT[weightClass]
    maskTable = MASK_NO_ZERO if isMostSignificant else MASK_ALL
    choices = range(1, 8) if isMostSignificant else range(8)
    forbiddenRow = FORBIDDEN_SHIFT[targetResidue]
    nextStates = {}

    for state, counts in states.items():
        forbiddenResidues = 0
        for previousClass in range(6):
            if previousClass == weightClass:
                continue
            previousBits = (state >> SHIFT[previousClass]) & CLASS_BITS
            usableMask = maskTable[previousBits]
            if usableMask:
                forbiddenResidues |= ROTATE[
                    forbiddenRow[previousClass][weightClass]
                ][usableMask]

        oldBits = (state >> shift) & CLASS_BITS
        for digitClass in choices:
            if forbiddenResidues & (1 << CLASS_RESIDUE[digitClass]):
                continue

            newBits = UPDATE_CLASS[oldBits][digitClass]
            newState = state ^ ((oldBits ^ newBits) << shift)
            add = ADD_CONTRIBUTION[weightClass][digitClass]
            multiplicity = CLASS_MULTIPLICITY[digitClass]
            permutation = PERMUTATION[add]

            current = nextStates.get(newState)
            if current is None:
                current = [0] * 7
                nextStates[newState] = current

            for residue in range(7):
                current[permutation[residue]] += counts[residue] * multiplicity

    return {state: tuple(counts) for state, counts in nextStates.items()}


@lru_cache(maxsize=None)
def countLengthResidue(length, targetResidue):
    states = {0: (1, 0, 0, 0, 0, 0, 0)}
    for position in range(length):
        states = advance(
            states,
            position,
            targetResidue,
            isMostSignificant=(position == length - 1),
        )
    return sum(counts[targetResidue] for counts in states.values())


def CPower10(exponent):
    total = 0
    for length in range(1, exponent + 1):
        for residue in range(1, 7):
            total += countLengthResidue(length, residue)
    return total


def solve():
    return CPower10(TARGET_EXPONENT)


def runTests():
    assert CPower10(2) == 74
    assert CPower10(4) == 3_737


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
