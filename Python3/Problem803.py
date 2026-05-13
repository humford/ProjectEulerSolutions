import time


A = 25_214_903_917
C = 11
MOD48 = 1 << 48
MASK48 = MOD48 - 1
MOD24 = 1 << 24
MASK24 = MOD24 - 1
MOD18 = 1 << 18
MASK18 = MOD18 - 1
INV9_MOD13 = 3
ORDER_EXP = 46


def charToValue(ch):
    code = ord(ch)
    if 97 <= code <= 122:
        return code - 97
    return code - 65 + 26


def valueToChar(value):
    if value < 26:
        return chr(97 + value)
    return chr(65 + value - 26)


def step48(state):
    return (A * state + C) & MASK48


def outputValue(state):
    return (state >> 16) % 52


def prefixFromSeed(seed, length):
    state = seed & MASK48
    chars = []
    for _ in range(length):
        chars.append(valueToChar(outputValue(state)))
        state = step48(state)
    return "".join(chars)


def firstOccurrenceBruteforce(seed, needle, limit):
    state = seed & MASK48
    window = []
    length = len(needle)

    for index in range(limit):
        window.append(valueToChar(outputValue(state)))
        if len(window) > length:
            window.pop(0)
        if len(window) == length and "".join(window) == needle:
            return index - length + 1
        state = step48(state)
    return -1


def u0Candidates(patternValues):
    needed = [value & 3 for value in patternValues]
    candidates = []

    for u0 in range(MOD18):
        u = u0
        ok = True
        for need in needed:
            if ((u >> 16) & 3) != need:
                ok = False
                break
            u = (A * u + C) & MASK18
        if ok:
            candidates.append(u0)

    return candidates


def solveY0ForResidues(carries24, residues13):
    length = len(residues13)
    r0 = residues13[0]

    if length == 1:
        return list(range(r0, MOD24, 13))

    r1 = residues13[1]
    a24 = A & MASK24
    delta1 = (13 * a24) & MASK24

    if length == 2:
        solutions = []
        y1 = (A * r0 + carries24[0]) & MASK24
        for y0 in range(r0, MOD24, 13):
            if y1 % 13 == r1:
                solutions.append(y0)
            y1 = (y1 + delta1) & MASK24
        return solutions

    r2 = residues13[2]
    y1 = (A * r0 + carries24[0]) & MASK24
    y2 = (A * y1 + carries24[1]) & MASK24
    delta2 = delta1 * a24 & MASK24

    solutions = []
    for y0 in range(r0, MOD24, 13):
        if y1 % 13 == r1 and y2 % 13 == r2:
            y = y2
            ok = True
            for i in range(2, length - 1):
                y = (A * y + carries24[i]) & MASK24
                if y % 13 != residues13[i + 1]:
                    ok = False
                    break
            if ok:
                solutions.append(y0)

        y1 = (y1 + delta1) & MASK24
        y2 = (y2 + delta2) & MASK24

    return solutions


def solveStatesForPattern(pattern):
    values = [charToValue(ch) for ch in pattern]
    length = len(values)
    states = []

    for u0 in u0Candidates(values):
        u = u0
        uList = [0] * length
        kList = [0] * (length - 1)

        for i in range(length):
            uList[i] = u
            nextValue = A * u + C
            if i < length - 1:
                kList[i] = nextValue >> 18
            u = nextValue & MASK18

        for w0 in range(64):
            w = w0
            carries24 = [0] * (length - 1)
            tList = [0] * length

            for i in range(length):
                tList[i] = ((uList[i] >> 16) & 3) + 4 * w
                if i < length - 1:
                    carries24[i] = (kList[i] + A * w) >> 6
                    w = (A * w + kList[i]) & 63

            residues13 = [
                INV9_MOD13 * ((values[i] - (tList[i] % 13)) % 13) % 13
                for i in range(length)
            ]

            for y0 in solveY0ForResidues(carries24, residues13):
                x0 = u0 + (w0 << 18)
                state = x0 + (y0 << 24)
                if prefixFromSeed(state, length) == pattern:
                    states.append(state)

    return states


def findUniqueSeedForPrefix(prefix):
    seeds = solveStatesForPattern(prefix)
    if len(seeds) != 1:
        raise RuntimeError("Expected a unique seed for %r, got %d" % (prefix, len(seeds)))
    return seeds[0]


G_ORDER2 = pow(A, 1 << (ORDER_EXP - 1), MOD48)
INV_POWS_2I = [pow(pow(A, 1 << i, MOD48), -1, MOD48) for i in range(ORDER_EXP)]


def dlogPower2BaseA(h):
    exponent = 0
    current = h % MOD48
    for bit in range(ORDER_EXP):
        test = pow(current, 1 << (ORDER_EXP - 1 - bit), MOD48)
        if test == G_ORDER2:
            exponent |= 1 << bit
            current = current * INV_POWS_2I[bit] % MOD48
        elif test != 1:
            raise RuntimeError("discrete log failed")
    return exponent


def powASumY(n):
    power = 1
    total = 0
    for bit in bin(n)[2:]:
        total = total * (1 + power) & MASK48
        power = power * power & MASK48
        if bit == "1":
            total = (total + power) & MASK48
            power = power * A & MASK48
    return power, total


def indexOfState(start, target):
    start &= MASK48
    target &= MASK48
    if start == target:
        return 0

    nextStart = step48(start)
    difference = (nextStart - start) & MASK48
    inverseDifference = pow(difference, -1, MOD48)
    yTarget = ((target - start) & MASK48) * inverseDifference % MOD48
    h = ((A - 1) * yTarget + 1) & MASK48

    baseIndex = dlogPower2BaseA(h)
    step = 1 << ORDER_EXP
    for lift in range(4):
        index = baseIndex + lift * step
        _, y = powASumY(index)
        if y == yTarget:
            return index

    raise RuntimeError("failed to lift discrete log")


def firstOccurrenceFromPrefix(startPrefix, needle):
    seed = findUniqueSeedForPrefix(startPrefix)
    targetStates = solveStatesForPattern(needle)
    return min(indexOfState(seed, state) for state in targetStates)


def runTests():
    assert prefixFromSeed(123456, 9) == "bQYicNGCY"
    assert firstOccurrenceBruteforce(123456, "RxqLBfWzv", 2000) == 100
    assert findUniqueSeedForPrefix("EULERcats") == 78_580_612_777_175


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = firstOccurrenceFromPrefix("PuzzleOne", "LuckyText")
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
