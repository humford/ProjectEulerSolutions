import time


MODULUS = 123_456_789
TARGET_N = 10**8
WEIGHT_PERIOD = 420
INDEX_MODULUS = 33_705
SEQUENCE_PREPERIOD = 54
SEQUENCE_PERIOD = 33_705
TOTIENT_LIMIT = 2_000_000


def sequenceMod(modulus, limit):
    values = [0] * (limit + 1)
    value = 1

    for index in range(1, limit + 1):
        values[index] = value
        value = ((value - 1) ** 3 + 2) % modulus

    return values


SEQUENCE_MOD_TARGET = sequenceMod(
    MODULUS,
    SEQUENCE_PREPERIOD + SEQUENCE_PERIOD,
)
SEQUENCE_MOD_WEIGHT_PERIOD = sequenceMod(INDEX_MODULUS, WEIGHT_PERIOD + 3)


def sequenceValueAtIndexMod(index):
    if index < SEQUENCE_PREPERIOD:
        return SEQUENCE_MOD_TARGET[index]

    reducedIndex = (
        SEQUENCE_PREPERIOD
        + (index - SEQUENCE_PREPERIOD) % SEQUENCE_PERIOD
    )
    return SEQUENCE_MOD_TARGET[reducedIndex]


def exactSmallSequenceValue(index):
    value = 1
    for _ in range(1, index):
        value = (value - 1) ** 3 + 2
    return value


def weight(gcdValue):
    if gcdValue < 5:
        return sequenceValueAtIndexMod(exactSmallSequenceValue(gcdValue))

    sequenceIndexMod = SEQUENCE_MOD_WEIGHT_PERIOD[
        3 + (gcdValue - 3) % WEIGHT_PERIOD
    ]
    return sequenceValueAtIndexMod(sequenceIndexMod)


WEIGHT_CYCLE_SUM = sum(
    weight(value)
    for value in range(5, 5 + WEIGHT_PERIOD)
) % MODULUS


def weightPrefixSum(limit):
    if limit <= 0:
        return 0

    total = 0
    smallLimit = min(limit, 4)
    for value in range(1, smallLimit + 1):
        total = (total + weight(value)) % MODULUS

    if limit <= 4:
        return total

    count = limit - 4
    cycles, remainder = divmod(count, WEIGHT_PERIOD)
    total = (total + cycles * WEIGHT_CYCLE_SUM) % MODULUS

    for value in range(5, 5 + remainder):
        total = (total + weight(value)) % MODULUS

    return total


def weightRangeSum(left, right):
    return (weightPrefixSum(right) - weightPrefixSum(left - 1)) % MODULUS


def totientPrefixTable(limit):
    phi = list(range(limit + 1))

    for value in range(2, limit + 1):
        if phi[value] == value:
            for multiple in range(value, limit + 1, value):
                phi[multiple] -= phi[multiple] // value

    prefix = [0] * (limit + 1)
    for value in range(1, limit + 1):
        prefix[value] = prefix[value - 1] + phi[value]

    return prefix


TOTIENT_PREFIX = totientPrefixTable(TOTIENT_LIMIT)
TOTIENT_SUM_CACHE = {}


def totientSum(limit):
    if limit <= TOTIENT_LIMIT:
        return TOTIENT_PREFIX[limit]

    cached = TOTIENT_SUM_CACHE.get(limit)
    if cached is not None:
        return cached

    total = limit * (limit + 1) // 2
    left = 2

    while left <= limit:
        quotient = limit // left
        right = limit // quotient
        total -= (right - left + 1) * totientSum(quotient)
        left = right + 1

    TOTIENT_SUM_CACHE[limit] = total
    return total


def coprimePairCount(limit):
    return (2 * totientSum(limit) - 1) % MODULUS


def T(limit):
    total = 0
    left = 1

    while left <= limit:
        quotient = limit // left
        right = limit // quotient
        total = (
            total
            + weightRangeSum(left, right) * coprimePairCount(quotient)
        ) % MODULUS
        left = right + 1

    return total


def solve():
    return T(TARGET_N)


def runTests():
    assert T(3) == 12
    assert T(4) == 24_881_925
    assert T(100) == 14_416_749
    assert solve() == 26_953_925


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
