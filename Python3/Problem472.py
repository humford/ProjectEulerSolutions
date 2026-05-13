import time


MODULUS = 100_000_000
PROBLEM_LIMIT = 10**12
BASE_LIMIT = 64


def edgeSegmentOccupants(length):
    if length <= 0:
        return 0

    target = length + 1
    power = 1 << (target.bit_length() - 1)
    return max(power >> 1, target - power)


def bruteWinningFirstChoices(seats):
    if seats == 1:
        return 1
    if seats == 2:
        return 2

    edgeCount = edgeSegmentOccupants(seats - 2)
    middleLength = seats - 3
    bestMiddle = -1
    middleChoices = 0

    for leftLength in range(middleLength + 1):
        count = edgeSegmentOccupants(leftLength)
        count += edgeSegmentOccupants(middleLength - leftLength)

        if count > bestMiddle:
            bestMiddle = count
            middleChoices = 1
        elif count == bestMiddle:
            middleChoices += 1

    best = max(edgeCount, bestMiddle)
    answer = 0
    if edgeCount == best:
        answer += 2
    if bestMiddle == best:
        answer += middleChoices
    return answer


BASE_VALUES = [0] * (BASE_LIMIT + 1)
BASE_PREFIX = [0] * (BASE_LIMIT + 1)

for seats in range(1, BASE_LIMIT + 1):
    BASE_VALUES[seats] = bruteWinningFirstChoices(seats)
    BASE_PREFIX[seats] = BASE_PREFIX[seats - 1] + BASE_VALUES[seats]


def winningFirstChoices(seats):
    if seats <= BASE_LIMIT:
        return BASE_VALUES[seats]

    power = 1 << (seats.bit_length() - 1)
    half = power >> 1
    split = power + half

    if seats >= split:
        offset = seats - split
        exponent = half.bit_length() - 1
        if exponent < 3:
            return bruteWinningFirstChoices(seats)

        quarter = half >> 1
        if offset == 0:
            return 4
        if offset <= quarter:
            return 2 * offset
        if offset == quarter + 1:
            return 3 * quarter + 3
        return half + 4 - offset

    offset = seats - power
    answer = winningFirstChoices(seats - half)
    exponent = half.bit_length() - 1

    if exponent >= 4:
        correctionStart = half - (half >> 2) + 1
        if offset >= correctionStart:
            answer += half - offset

    return answer


SUM_CACHE = {}


def prefixElevenBlock(half, length):
    if length <= 0:
        return 0

    exponent = half.bit_length() - 1
    if exponent < 3:
        start = 3 * half
        return sum(bruteWinningFirstChoices(seats) for seats in range(start, start + length))

    quarter = half >> 1
    total = 4
    length -= 1
    if length == 0:
        return total

    take = min(quarter, length)
    total += take * (take + 1)
    length -= take
    position = take
    if length == 0:
        return total

    if position == quarter:
        total += 3 * quarter + 3
        length -= 1
        position += 1
        if length == 0:
            return total

    first = quarter + 2
    count = length
    total += count * (2 * first - count + 1) // 2
    return total


def winningChoiceSum(limit):
    if limit <= BASE_LIMIT:
        return BASE_PREFIX[limit] % MODULUS
    if limit in SUM_CACHE:
        return SUM_CACHE[limit]

    power = 1 << (limit.bit_length() - 1)
    half = power >> 1
    split = power + half
    total = winningChoiceSum(power - 1)

    if limit < split:
        offset = limit - power
        mapped = winningChoiceSum(half + offset) - winningChoiceSum(half - 1)

        exponent = half.bit_length() - 1
        if exponent >= 4:
            correctionStart = half - (half >> 2) + 1
            if offset >= correctionStart:
                count = offset - correctionStart + 1
                correction = count * half
                correction -= (correctionStart + offset) * count // 2
                mapped += correction

        total = (total + mapped) % MODULUS
        SUM_CACHE[limit] = total
        return total

    tenBlock = winningChoiceSum(power - 1) - winningChoiceSum(half - 1)
    exponent = half.bit_length() - 1
    if exponent >= 4:
        tailLength = (half >> 2) - 1
        tenBlock += tailLength * (tailLength + 1) // 2
    else:
        tenBlock = sum(bruteWinningFirstChoices(seats) for seats in range(power, split))

    total = (total + tenBlock) % MODULUS
    elevenLength = limit - split + 1
    total = (total + prefixElevenBlock(half, elevenLength)) % MODULUS
    SUM_CACHE[limit] = total
    return total


def runTests():
    for seats in range(1, 1_001):
        assert winningFirstChoices(seats) == bruteWinningFirstChoices(seats)

    assert winningFirstChoices(1) == 1
    assert winningFirstChoices(15) == 9
    assert winningFirstChoices(20) == 6
    assert winningFirstChoices(500) == 16
    assert winningChoiceSum(20) == 83
    assert winningChoiceSum(500) == 13_343


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningChoiceSum(PROBLEM_LIMIT) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer).zfill(8) + " in " + str(elapsed) + " seconds.")
