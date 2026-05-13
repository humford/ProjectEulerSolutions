from functools import lru_cache
import math
import time


MAX_LENGTH = 90
PRIMITIVE_SEARCH_LIMIT = 500_000
LOG_2 = math.log(2)
LOG_3 = math.log(3)
POWERS_OF_THREE = [1]

for _ in range(MAX_LENGTH + 2):
    POWERS_OF_THREE.append(POWERS_OF_THREE[-1] * 3)


def isPowerOfTwo(n):
    return n > 0 and n & (n - 1) == 0


def fibonacci(n):
    if n < 1:
        return 0

    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b

    return b


def collatzPrefix(start, maxLength):
    values = [start]
    operations = []
    current = start

    while len(values) <= maxLength:
        if current % 2 == 0:
            nextValue = current // 2
            operation = "d"
        else:
            nextValue = 3 * current + 1
            operation = "u"

        if isPowerOfTwo(nextValue):
            return "".join(operations), values

        operations.append(operation)
        values.append(nextValue)
        current = nextValue

    return None, None


def rankPattern(values):
    ranks = [0] * len(values)
    for rank, (_, index) in enumerate(sorted((value, index) for index, value in enumerate(values))):
        ranks[index] = rank

    return tuple(ranks)


def slopeScores(operations):
    twos, threes = 0, 1
    reversedScores = [twos * LOG_2 - threes * LOG_3]

    for operation in reversed(operations):
        if operation == "d":
            twos += 1
        else:
            threes += 1

        reversedScores.append(twos * LOG_2 - threes * LOG_3)

    return list(reversed(reversedScores))


def isExceptionalPrefix(operations, values):
    return rankPattern(values) != rankPattern(slopeScores(operations))


def validPrimitiveExtension(prefix, primitiveStart):
    current = primitiveStart

    for operation in reversed(prefix):
        if operation == "d":
            current *= 2
        else:
            if (current - 1) % 3 != 0:
                return False

            current = (current - 1) // 3
            if current <= 0 or current % 2 == 0 or isPowerOfTwo(current):
                return False

    return True


def isDescendantOfPrimitive(operations, primitives):
    for primitiveLength, primitiveStart, primitiveOperations in primitives:
        if operations == primitiveOperations:
            return True

        if len(operations) <= len(primitiveOperations):
            continue

        if not operations.endswith(primitiveOperations):
            continue

        prefix = operations[: -len(primitiveOperations)]
        if validPrimitiveExtension(prefix, primitiveStart):
            return True

    return False


@lru_cache(maxsize=None)
def primitiveExceptionalSeeds(targetLength, searchLimit):
    candidates = []

    for start in range(2, searchLimit + 1):
        operations, values = collatzPrefix(start, targetLength)
        if operations is None:
            continue

        length = len(values)
        if length <= targetLength and isExceptionalPrefix(operations, values):
            candidates.append((length, start, operations))

    primitives = []
    for length, start, operations in sorted(candidates):
        if not isDescendantOfPrimitive(operations, primitives):
            primitives.append((length, start, operations))

    return tuple(primitives)


def neededResiduePower(remainingLength):
    return remainingLength // 2 + 1


@lru_cache(maxsize=None)
def reverseExtensionCount(residue, remainingLength):
    if remainingLength == 0:
        return 1

    modulus = POWERS_OF_THREE[neededResiduePower(remainingLength)]
    residue %= modulus

    shorterModulus = POWERS_OF_THREE[neededResiduePower(remainingLength - 1)]
    total = reverseExtensionCount((2 * residue) % shorterModulus, remainingLength - 1)

    if remainingLength >= 2 and residue % 3 == 2:
        reducedModulus = POWERS_OF_THREE[neededResiduePower(remainingLength - 2)]
        reduced = ((2 * residue - 1) // 3) % reducedModulus
        total += reverseExtensionCount(reduced, remainingLength - 2)

    return total


def exceptionalFamilyCount(length):
    primitives = primitiveExceptionalSeeds(MAX_LENGTH, PRIMITIVE_SEARCH_LIMIT)
    total = 0

    for primitiveLength, primitiveStart, _ in primitives:
        if primitiveLength <= length:
            total += reverseExtensionCount(primitiveStart, length - primitiveLength)

    return total


def collatzPrefixFamilies(length):
    return fibonacci(length) + exceptionalFamilyCount(length)


def runTests():
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55
    assert collatzPrefixFamilies(5) == 5
    assert collatzPrefixFamilies(10) == 55
    assert collatzPrefixFamilies(20) == 6_771

    primitives = primitiveExceptionalSeeds(MAX_LENGTH, PRIMITIVE_SEARCH_LIMIT)
    assert tuple((length, start) for length, start, _ in primitives) == (
        (15, 9),
        (16, 19),
        (17, 37),
        (20, 51),
        (50, 159),
        (81, 155),
    )


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = collatzPrefixFamilies(90)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
