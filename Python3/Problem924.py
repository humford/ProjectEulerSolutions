import time


MODULUS = 1_000_000_007
TARGET_N = 10**16
SUFFIX_DIGITS = 11
SUFFIX_MODULUS = 10**SUFFIX_DIGITS
SUFFIX_PREPERIOD = 5
SUFFIX_PERIOD = 15_625_000


def nextPermutationValue(n):
    digits = list(str(n))
    pivot = len(digits) - 2

    while pivot >= 0 and digits[pivot] >= digits[pivot + 1]:
        pivot -= 1

    if pivot < 0:
        return 0

    swapIndex = len(digits) - 1
    while digits[swapIndex] <= digits[pivot]:
        swapIndex -= 1

    digits[pivot], digits[swapIndex] = digits[swapIndex], digits[pivot]
    digits[pivot + 1:] = reversed(digits[pivot + 1:])

    return int("".join(digits))


def exactU(n):
    a = 0
    total = 0

    for _ in range(n):
        a = a * a + 2
        total = (total + nextPermutationValue(a)) % MODULUS

    return total


def suffixPermutationDelta(suffix):
    digits = list(f"{suffix:0{SUFFIX_DIGITS}d}")
    pivot = SUFFIX_DIGITS - 2

    while pivot >= 0 and digits[pivot] >= digits[pivot + 1]:
        pivot -= 1

    if pivot < 0:
        raise ValueError("suffix width is too small")

    swapIndex = SUFFIX_DIGITS - 1
    while digits[swapIndex] <= digits[pivot]:
        swapIndex -= 1

    digits[pivot], digits[swapIndex] = digits[swapIndex], digits[pivot]
    digits[pivot + 1:] = reversed(digits[pivot + 1:])

    return int("".join(digits)) - suffix


def recurrencePeriodData(modulus):
    a = 0
    seen = {0: 0}
    values = []

    while True:
        a = (a * a + 2) % modulus
        values.append(a)

        if a in seen:
            return values, seen[a], len(values) - seen[a]

        seen[a] = len(values)


def recurrenceSumModulo(n, modulus):
    values, preperiod, period = recurrencePeriodData(modulus)

    if n <= len(values):
        return sum(values[:n]) % MODULUS

    total = sum(values[:preperiod]) % MODULUS
    remaining = n - preperiod
    cycle = values[preperiod:preperiod + period]

    return (
        total
        + (remaining // period % MODULUS) * (sum(cycle) % MODULUS)
        + sum(cycle[:remaining % period])
    ) % MODULUS


def firstValues(count):
    a = 0
    values = []

    for _ in range(count):
        a = a * a + 2
        values.append(a)

    return values


def suffixDeltaPeriodAndPrefix(remainder):
    a = 0
    for _ in range(SUFFIX_PREPERIOD):
        a = (a * a + 2) % SUFFIX_MODULUS

    periodSum = 0
    prefixSum = 0

    for index in range(1, SUFFIX_PERIOD + 1):
        a = (a * a + 2) % SUFFIX_MODULUS
        delta = suffixPermutationDelta(a) % MODULUS

        periodSum += delta
        if periodSum >= 1 << 63:
            periodSum %= MODULUS

        if index <= remainder:
            prefixSum += delta
            if prefixSum >= 1 << 63:
                prefixSum %= MODULUS

    return periodSum % MODULUS, prefixSum % MODULUS


def U(n):
    if n <= SUFFIX_PREPERIOD:
        return exactU(n)

    initialValues = firstValues(SUFFIX_PREPERIOD)
    initialNextPermutationSum = sum(nextPermutationValue(value) for value in initialValues) % MODULUS
    initialRecurrenceSum = sum(initialValues) % MODULUS

    recurrenceTailSum = (
        recurrenceSumModulo(n, MODULUS) - initialRecurrenceSum
    ) % MODULUS

    tailCount = n - SUFFIX_PREPERIOD
    fullPeriods, remainder = divmod(tailCount, SUFFIX_PERIOD)
    periodSum, prefixSum = suffixDeltaPeriodAndPrefix(remainder)
    deltaSum = ((fullPeriods % MODULUS) * periodSum + prefixSum) % MODULUS

    return (initialNextPermutationSum + recurrenceTailSum + deltaSum) % MODULUS


def solve():
    return U(TARGET_N)


def runTests():
    assert nextPermutationValue(245) == 254
    assert nextPermutationValue(542) == 0
    assert suffixPermutationDelta(4_371_938_082_726 % SUFFIX_MODULUS) == 36
    assert exactU(10) == 543_870_437
    assert U(10) == 543_870_437
    assert recurrencePeriodData(SUFFIX_MODULUS)[1:] == (SUFFIX_PREPERIOD, SUFFIX_PERIOD)
    assert solve() == 811_141_860


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
