import time
from array import array


LIMIT = 10**6


def precomputeGolomb(productLimit):
    golomb = array("I", [0, 1])
    productSum = 1
    index = 2

    while productSum < productLimit:
        current = 1 + golomb[index - golomb[golomb[index - 1]]]
        golomb.append(current)
        productSum += index * current
        index += 1

    return golomb


def golombValue(number):
    golomb = precomputeGolomb(number)
    index = 1
    previousValueSum = 0
    valueSum = 1
    previousProductSum = 0
    productSum = 1

    while productSum < number:
        index += 1
        previousValueSum = valueSum
        valueSum += golomb[index]
        previousProductSum = productSum
        productSum += index * golomb[index]

    return previousValueSum + (number - previousProductSum + index - 1) // index


def golombCubeSum(limit=LIMIT):
    golomb = precomputeGolomb(limit**3)
    index = 1
    previousValueSum = 0
    valueSum = 1
    previousProductSum = 0
    productSum = 1
    total = 0

    for number in range(1, limit):
        cube = number * number * number

        while productSum < cube:
            index += 1
            previousValueSum = valueSum
            valueSum += golomb[index]
            previousProductSum = productSum
            productSum += index * golomb[index]

        total += previousValueSum + (cube - previousProductSum + index - 1) // index

    return total


def runTests():
    assert golombValue(10**3) == 86
    assert golombValue(10**6) == 6137
    assert golombCubeSum(10**3) == 153506976


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = golombCubeSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
