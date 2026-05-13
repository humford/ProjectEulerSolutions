import time
from bisect import bisect_right


MOD = 1_000_000_007


def fourthRootFloor(n):
    root = int(n ** 0.25)
    while (root + 1) ** 4 <= n:
        root += 1
    while root ** 4 > n:
        root -= 1
    return root


def totientSieve(limit):
    phi = list(range(limit + 1))
    for n in range(2, limit + 1):
        if phi[n] == n:
            for multiple in range(n, limit + 1, n):
                phi[multiple] -= phi[multiple] // n
    return phi


def countConsecutive(limit):
    if limit < 5:
        return 0
    return (limit - 4) * (limit - 3) // 2


def countGeometric(limit, phi):
    total = 0
    for ratioTop in range(2, fourthRootFloor(limit) + 1):
        power = ratioTop ** 4
        while power <= limit:
            total += phi[ratioTop] * (limit // power)
            power *= ratioTop
    return total


def recurrenceLength(first, second, multiplier, sign, limit):
    length = 2
    previous, current = first, second
    while True:
        nextValue = multiplier * current + sign * previous
        if nextValue > limit:
            return length
        previous, current = current, nextValue
        length += 1


def countSubsequencesFromLength(length):
    if length < 5:
        return 0
    return (length - 4) * (length - 3) // 2


def countRecurrenceFamily(first, second, multiplier, sign, limit):
    return countSubsequencesFromLength(recurrenceLength(first, second, multiplier, sign, limit))


def countRegular(limit):
    total = countRecurrenceFamily(1, 2, 1, 1, limit)
    maxMultiplier = fourthRootFloor(limit) + 2

    for multiplier in range(2, maxMultiplier + 1):
        total += countSubsequencesFromLength(
            recurrenceLength(1, multiplier, multiplier, 1, limit)
        )

    total += countRecurrenceFamily(1, 3, 2, 1, limit)

    for multiplier in range(3, maxMultiplier + 1):
        total += countSubsequencesFromLength(
            recurrenceLength(1, multiplier, multiplier, -1, limit)
        )

    total += countRecurrenceFamily(1, 2, 3, -1, limit)
    total += countRecurrenceFamily(1, 3, 4, -1, limit)
    return total


def isConsecutive(sequence):
    return all(sequence[i + 1] == sequence[i] + 1 for i in range(len(sequence) - 1))


def isGeometric(sequence):
    return all(
        sequence[i + 1] * sequence[0] == sequence[i] * sequence[1]
        for i in range(1, len(sequence) - 1)
    )


def followsRecurrence(sequence, multiplier, sign):
    return all(
        sequence[i + 1] == multiplier * sequence[i] + sign * sequence[i - 1]
        for i in range(1, len(sequence) - 1)
    )


def inKnownFamily(sequence):
    if isConsecutive(sequence) or isGeometric(sequence):
        return True

    first, second, third = sequence[0], sequence[1], sequence[2]
    if (third - first) % second == 0:
        multiplier = (third - first) // second
        error = second * second - first * (multiplier * second + first)
        if multiplier >= 1 and abs(error) <= 2 and followsRecurrence(sequence, multiplier, 1):
            return True

    if (third + first) % second == 0:
        multiplier = (third + first) // second
        error = second * second - first * (multiplier * second - first)
        if multiplier >= 2 and abs(error) <= 2 and followsRecurrence(sequence, multiplier, -1):
            return True

    return False


def finiteExceptionMaxes(bound):
    found = []
    for start in ([1, 2], [2, 3]):
        stack = [start]
        while stack:
            sequence = stack.pop()
            if sequence[-1] > bound:
                continue
            if len(sequence) >= 5 and not inKnownFamily(sequence):
                found.append(sequence)

            a, b = sequence[-2], sequence[-1]
            square = b * b
            for error in (-2, -1, 0, 1, 2):
                numerator = square + error
                if numerator % a:
                    continue
                c = numerator // a
                if b < c <= bound:
                    stack.append(sequence + [c])

    infinitePath = [1, 2, 6]
    while infinitePath[-1] * 3 <= bound:
        infinitePath.append(infinitePath[-1] * 3)
    infinitePrefixes = {tuple(infinitePath[:length]) for length in range(5, len(infinitePath) + 1)}

    return sorted(sequence[-1] for sequence in found if tuple(sequence) not in infinitePrefixes)


def infiniteExceptionCount(limit):
    if limit < 2:
        return 0
    length = 1
    value = 2
    while value <= limit:
        length += 1
        value *= 3
    return max(0, length - 4)


def countExceptions(limit, finiteMaxes):
    return bisect_right(finiteMaxes, limit) + infiniteExceptionCount(limit)


def G(limit, phi, finiteMaxes):
    return (
        countConsecutive(limit)
        + countGeometric(limit, phi)
        + countRegular(limit)
        + countExceptions(limit, finiteMaxes)
    ) % MOD


def runTests():
    phi = totientSieve(fourthRootFloor(10 ** 18) + 2)
    exceptions = finiteExceptionMaxes(1_000)
    assert G(6, phi, exceptions) == 4
    assert G(10, phi, exceptions) == 26
    assert G(100, phi, exceptions) == 4_710
    assert G(1_000, phi, exceptions) == 496_805
    return phi, exceptions


if __name__ == "__main__":
    start = time.time()
    phi, exceptions = runTests()
    answer = G(10 ** 18, phi, exceptions)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
