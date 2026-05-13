import time


MODULUS = 1_000_000_033


def bottleRemovalValuesUpTo(maxLayers, modulus=MODULUS):
    if maxLayers < 1:
        return [0]

    oddInverses = [0] * (maxLayers + 1)
    for layer in range(1, maxLayers + 1):
        oddInverses[layer] = pow(2 * layer - 1, modulus - 2, modulus)

    values = [0] * (maxLayers + 1)
    values[1] = 1

    currentBottleCount = 1
    currentValue = 1
    powerOfTwo = 2
    mersennePrefix = 1
    oddInversePrefix = 1

    for layer in range(2, maxLayers + 1):
        for factor in range(currentBottleCount + 1, currentBottleCount + layer + 1):
            currentValue = currentValue * factor % modulus
        currentBottleCount += layer

        powerOfTwo = powerOfTwo * 2 % modulus
        mersennePrefix = mersennePrefix * (powerOfTwo - 1) % modulus
        oddInversePrefix = oddInversePrefix * oddInverses[layer] % modulus

        currentValue = currentValue * mersennePrefix % modulus
        currentValue = currentValue * oddInversePrefix % modulus
        values[layer] = currentValue

    return values


def bottleRemovalCount(layers):
    return bottleRemovalValuesUpTo(layers)[layers]


def bottleRemovalPrefix(layers, modulus=MODULUS):
    if layers < 1:
        return 0

    oddInverses = [0] * (layers + 1)
    for layer in range(1, layers + 1):
        oddInverses[layer] = pow(2 * layer - 1, modulus - 2, modulus)

    currentBottleCount = 1
    currentValue = 1
    total = 1
    powerOfTwo = 2
    mersennePrefix = 1
    oddInversePrefix = 1

    for layer in range(2, layers + 1):
        for factor in range(currentBottleCount + 1, currentBottleCount + layer + 1):
            currentValue = currentValue * factor % modulus
        currentBottleCount += layer

        powerOfTwo = powerOfTwo * 2 % modulus
        mersennePrefix = mersennePrefix * (powerOfTwo - 1) % modulus
        oddInversePrefix = oddInversePrefix * oddInverses[layer] % modulus

        currentValue = currentValue * mersennePrefix % modulus
        currentValue = currentValue * oddInversePrefix % modulus
        total = (total + currentValue) % modulus

    return total


def runTests():
    assert bottleRemovalCount(1) == 1
    assert bottleRemovalCount(2) == 6
    assert bottleRemovalCount(3) == 1_008


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = bottleRemovalPrefix(10**4)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
