import time


MOD = 1_000_062_031


def b(n):
    return n & -n


def maxBinomialBitLength(r):
    coefficient = 1
    result = 1

    for k in range(r + 1):
        result = max(result, coefficient.bit_length())
        if k < r:
            coefficient = coefficient * (r - k) // (k + 1)

    return result


def onePositionsFromBinomial(t, r):
    positions = []
    coefficient = 1

    for k in range(r + 1):
        value = coefficient
        while value:
            lowestBit = value & -value
            positions.append(k * t + lowestBit.bit_length() - 1)
            value -= lowestBit

        if k < r:
            coefficient = coefficient * (r - k) // (k + 1)

    return positions


def addShiftedPositions(positions, shift):
    i = 0
    j = 0
    previous = -1
    carry = False
    result = []

    while i < len(positions) or j < len(positions) or carry:
        candidates = []
        if i < len(positions):
            candidates.append(positions[i])
        if j < len(positions):
            candidates.append(positions[j] + shift)
        if carry:
            candidates.append(previous + 1)

        position = min(candidates)
        total = 0

        if i < len(positions) and positions[i] == position:
            total += 1
            i += 1
        if j < len(positions) and positions[j] + shift == position:
            total += 1
            j += 1
        if carry and position == previous + 1:
            total += 1
            carry = False

        if total % 2:
            result.append(position)
        carry = total >= 2
        previous = position

    return result


def onePositionsPower(t, r):
    if r == 0:
        return [0]

    if t >= maxBinomialBitLength(r):
        return onePositionsFromBinomial(t, r)

    positions = [0]
    for _ in range(r):
        positions = addShiftedPositions(positions, t)

    return positions


def AFromPositions(positions, modulus=None):
    if len(positions) == 1:
        return 1 if modulus is None else 1 % modulus

    if any(positions[i] >= positions[i + 1] for i in range(len(positions) - 1)):
        positions = sorted(set(positions))

    valueByOnesSeen = [1] * len(positions)
    for i in range(1, len(positions)):
        value = 5 * valueByOnesSeen[i - 1] + 3
        valueByOnesSeen[i] = value if modulus is None else value % modulus

    result = 1 if modulus is None else 1 % modulus
    descending = positions[::-1]

    for i in range(len(descending) - 1):
        zeroRun = descending[i] - descending[i + 1] - 1
        if zeroRun <= 0:
            continue

        base = valueByOnesSeen[i + 1]
        if modulus is None:
            result *= base ** zeroRun
        else:
            result = result * pow(base, zeroRun, modulus) % modulus

    return result


def ASlow(n):
    memo = {0: 1}

    def recurse(x):
        if x in memo:
            return memo[x]
        if x % 2:
            result = recurse(x // 2)
        else:
            half = x // 2
            result = 3 * recurse(half) + 5 * recurse(x - b(half))
        memo[x] = result
        return result

    return recurse(n)


def H(t, r, modulus=MOD):
    return AFromPositions(onePositionsPower(t, r), modulus)


def runTests():
    assert b(24) == 8
    assert ASlow(0) == 1
    assert H(3, 2, None) == 636_056
    assert ASlow(81) == 636_056


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = H(10 ** 14 + 31, 62, MOD)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
