import time
from functools import cache


MODULUS = 10 ** 9
POWER_OF_TWO_MODULUS = 2 ** 9
ODD_MODULUS = 5 ** 9

BASE_FACTORS = {
    1: ["1"],
    2: ["10", "11"],
    3: ["100", "101", "110"],
}


def thueMorsePrefix(length):
    return "".join(str(number.bit_count() & 1) for number in range(length))


def appearsInThueMorse(number, prefix):
    return bin(number)[2:] in prefix


def bruteA(index, prefixLength=200000):
    prefix = thueMorsePrefix(prefixLength)
    found = []
    number = 0

    while len(found) <= index:
        if appearsInThueMorse(number, prefix):
            found.append(number)

        number += 1

    return found[index]


@cache
def factorCount(length):
    if length <= 0:
        return 0
    if length <= 3:
        return len(BASE_FACTORS[length])
    if length % 2 == 0:
        half = length // 2
        return factorCount(half) + factorCount(half + 1)

    return 2 * factorCount((length + 1) // 2)


@cache
def factorsThroughLength(length):
    if length <= 0:
        return 0
    if length == 1:
        return 1
    if length == 2:
        return 3
    if length == 3:
        return 6

    if length % 2 == 0:
        half = length // 2
        return 3 * factorsThroughLength(half) + factorsThroughLength(half + 1) - 4

    half = (length + 1) // 2
    return (
        3 * factorsThroughLength(half)
        + factorsThroughLength(half + 1)
        - 4
        - factorCount(half)
        - factorCount(half + 1)
    )


def baseNode(bits):
    return ("base", bits, len(bits))


def operationNode(operation, child, length):
    return (operation, child, length)


def nodeLength(node):
    return node[2]


def selectFactorOfLength(length, offset):
    if length <= 3:
        return baseNode(BASE_FACTORS[length][offset])

    if length % 2 == 1:
        parentLength = (length + 1) // 2
        halfCount = factorCount(parentLength)
        if offset < halfCount:
            return operationNode("B", selectFactorOfLength(parentLength, offset), length)

        reversedOffset = halfCount - 1 - (offset - halfCount)
        return operationNode("C", selectFactorOfLength(parentLength, reversedOffset), length)

    parentLength = length // 2
    firstCount = factorCount(parentLength)
    if offset < firstCount:
        return operationNode("A", selectFactorOfLength(parentLength, offset), length)

    reversedOffset = factorCount(parentLength + 1) - 1 - (offset - firstCount)
    return operationNode("D", selectFactorOfLength(parentLength + 1, reversedOffset), length)


def selectFactor(index):
    if index == 0:
        return None

    lower = 1
    upper = 1
    while factorsThroughLength(upper) < index:
        upper *= 2

    while lower < upper:
        middle = (lower + upper) // 2
        if factorsThroughLength(middle) >= index:
            upper = middle
        else:
            lower = middle + 1

    length = lower
    offset = index - factorsThroughLength(length - 1) - 1
    return selectFactorOfLength(length, offset)


def morseImage(bits):
    return "".join("10" if bit == "1" else "01" for bit in bits)


def complementMorseImage(bits):
    return "".join("01" if bit == "1" else "10" for bit in bits)


def factorBits(node):
    if node is None:
        return "0"

    operation = node[0]
    if operation == "base":
        return node[1]

    bits = factorBits(node[1])
    if operation == "A":
        return morseImage(bits)
    if operation == "B":
        return morseImage(bits)[:-1]
    if operation == "C":
        return complementMorseImage(bits)[1:]
    if operation == "D":
        return complementMorseImage(bits)[1:-1]

    raise ValueError("Unknown operation " + operation)


def firstBit(node):
    if node[0] == "base":
        return int(node[1][0])

    return firstBit(node[1])


def lastBit(node):
    operation = node[0]
    if operation == "base":
        return int(node[1][-1])

    child = node[1]
    if operation == "A":
        return 1 - lastBit(child)
    if operation == "B" or operation == "C":
        return lastBit(child)
    if operation == "D":
        return 1 - lastBit(child)

    raise ValueError("Unknown operation " + operation)


@cache
def powerAndGeometricSum(base, exponent):
    if exponent == 0:
        return 1, 0

    if exponent % 2 == 0:
        halfPower, halfSum = powerAndGeometricSum(base, exponent // 2)
        return (
            halfPower * halfPower % ODD_MODULUS,
            halfSum * (1 + halfPower) % ODD_MODULUS,
        )

    previousPower, previousSum = powerAndGeometricSum(base, exponent - 1)
    return (
        previousPower * base % ODD_MODULUS,
        (previousSum + previousPower) % ODD_MODULUS,
    )


@cache
def valueModOddPart(node, base):
    operation = node[0]
    if operation == "base":
        value = 0
        for bit in node[1]:
            value = (value * base + int(bit)) % ODD_MODULUS
        return value

    child = node[1]
    childLength = nodeLength(child)
    nextBase = base * base % ODD_MODULUS
    _, geometricSum = powerAndGeometricSum(nextBase, childLength)
    childValue = valueModOddPart(child, nextBase)

    imageValue = (geometricSum + (base - 1) * childValue) % ODD_MODULUS
    if operation == "A":
        return imageValue

    inverseBase = pow(base, -1, ODD_MODULUS)
    if operation == "B":
        return (imageValue - (1 - lastBit(child))) * inverseBase % ODD_MODULUS

    complementValue = (base * geometricSum + (1 - base) * childValue) % ODD_MODULUS
    droppedFirst = 1 - firstBit(child)
    if droppedFirst:
        complementValue -= droppedFirst * pow(base, 2 * childLength - 1, ODD_MODULUS)
        complementValue %= ODD_MODULUS

    if operation == "C":
        return complementValue

    if operation == "D":
        return (complementValue - lastBit(child)) * inverseBase % ODD_MODULUS

    raise ValueError("Unknown operation " + operation)


def trailingBits(node, bitCount):
    if nodeLength(node) <= bitCount:
        return factorBits(node)

    operation = node[0]
    if operation == "base":
        return node[1][-bitCount:]

    child = node[1]
    if operation == "A":
        return morseImage(trailingBits(child, (bitCount + 1) // 2))[-bitCount:]
    if operation == "B":
        return morseImage(trailingBits(child, (bitCount + 2) // 2))[:-1][-bitCount:]
    if operation == "C":
        return complementMorseImage(trailingBits(child, (bitCount + 1) // 2))[-bitCount:]
    if operation == "D":
        return complementMorseImage(trailingBits(child, (bitCount + 2) // 2))[:-1][-bitCount:]

    raise ValueError("Unknown operation " + operation)


def combineResidues(powerOfTwoResidue, oddResidue):
    multiplier = (
        (powerOfTwoResidue - oddResidue)
        * pow(ODD_MODULUS, -1, POWER_OF_TWO_MODULUS)
        % POWER_OF_TWO_MODULUS
    )
    return (oddResidue + ODD_MODULUS * multiplier) % MODULUS


def factorValueMod(node):
    if node is None:
        return 0

    powerOfTwoResidue = int(trailingBits(node, 9), 2) % POWER_OF_TWO_MODULUS
    oddResidue = valueModOddPart(node, 2)
    return combineResidues(powerOfTwoResidue, oddResidue)


def aValue(index):
    return int(factorBits(selectFactor(index)), 2)


def aValueMod(index):
    return factorValueMod(selectFactor(index))


def thueMorseSubsequenceAnswer():
    return sum(aValueMod(10 ** exponent) for exponent in range(1, 19)) % MODULUS


def runTests():
    prefix = thueMorsePrefix(1000)
    expected = [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 18]

    assert [number for number in range(19) if appearsInThueMorse(number, prefix)] == expected
    assert [aValue(index) for index in range(13)] == expected
    assert bruteA(100) == 3251
    assert aValue(100) == 3251
    assert aValue(1000) == 80852364498


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = thueMorseSubsequenceAnswer()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
