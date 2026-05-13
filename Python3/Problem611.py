import time
from array import array
from math import isqrt


def bruteOpenDoorCount(limit):
    toggled = bytearray(limit + 1)
    root = isqrt(limit)

    for a in range(1, root + 1):
        aSquared = a * a
        for b in range(a + 1, root + 1):
            door = aSquared + b * b
            if door > limit:
                break
            toggled[door] ^= 1

    return sum(toggled)


def smallestPrimeFactorSieve(limit):
    spf = array("I", [0]) * (limit + 1)
    primes = []

    for number in range(2, limit + 1):
        if spf[number] == 0:
            spf[number] = number
            primes.append(number)

        for prime in primes:
            product = number * prime
            if product > limit:
                break
            spf[product] = prime
            if prime == spf[number]:
                break

    return spf, primes


def oneModFourPrimePrefix(limit, primes):
    isPrime = bytearray(limit + 1)
    for prime in primes:
        isPrime[prime] = 1

    prefix = array("I", [0]) * (limit + 1)
    count = 0
    for number in range(limit + 1):
        if isPrime[number] and number % 4 == 1:
            count += 1
        prefix[number] = count

    return prefix


def primeAndCharacterTables(limit, primes, root):
    values = array("q")
    index = 1
    while index <= limit:
        quotient = limit // index
        values.append(quotient)
        index = limit // quotient + 1

    bigIndex = array("I", [0]) * (root + 1)
    for index, value in enumerate(values):
        if value <= root:
            break
        bigIndex[limit // value] = index

    primeCounts = array("q", [0]) * len(values)
    characterSums = array("q", [0]) * len(values)
    for index, value in enumerate(values):
        primeCounts[index] = value - 1 if value >= 2 else 0
        integerCharacterSum = ((value + 3) // 4) - ((value + 1) // 4)
        characterSums[index] = integerCharacterSum - 1

    def firstIndexBelow(threshold):
        low = 0
        high = len(values)
        while low < high:
            middle = (low + high) // 2
            if values[middle] >= threshold:
                low = middle + 1
            else:
                high = middle
        return low

    valueCount = len(values)
    for prime in primes:
        primeSquared = prime * prime
        if primeSquared > limit:
            break

        updateCount = firstIndexBelow(primeSquared)
        baseIndex = valueCount - (prime - 1)
        basePrimeCount = primeCounts[baseIndex]
        baseCharacterSum = characterSums[baseIndex]
        primeCharacter = 0 if prime == 2 else (1 if prime % 4 == 1 else -1)

        for index in range(updateCount):
            reducedValue = values[index] // prime
            if reducedValue <= root:
                reducedIndex = valueCount - reducedValue
            else:
                reducedIndex = bigIndex[limit // reducedValue]

            primeCounts[index] -= primeCounts[reducedIndex] - basePrimeCount
            if primeCharacter:
                characterSums[index] -= primeCharacter * (
                    characterSums[reducedIndex] - baseCharacterSum
                )

    return values, bigIndex, primeCounts, characterSums


def oddOneModFourPrimeParity(number, spf):
    parity = 0
    excludedPrimes = []

    while number > 1:
        prime = spf[number]
        oddExponent = False
        while number % prime == 0:
            number //= prime
            oddExponent = not oddExponent
        if oddExponent and prime % 4 == 1:
            parity ^= 1
            excludedPrimes.append(prime)

    return parity, excludedPrimes


def openDoorCount(limit):
    root = isqrt(limit)
    spf, primes = smallestPrimeFactorSieve(root)
    smallOneModFourPrimeCounts = oneModFourPrimePrefix(root, primes)
    values, bigIndex, primeCounts, characterSums = primeAndCharacterTables(
        limit, primes, root
    )
    valueCount = len(values)

    def oneModFourPrimeCount(x):
        if x < 5:
            return 0
        if x <= root:
            return smallOneModFourPrimeCounts[x]

        tableIndex = bigIndex[limit // x]
        return (primeCounts[tableIndex] - 1 + characterSums[tableIndex]) // 2

    total = 0
    for oddRoot in range(1, root + 1, 2):
        oddRootSquared = oddRoot * oddRoot
        maxMultiplier = limit // oddRootSquared
        parity, excludedPrimes = oddOneModFourPrimeParity(oddRoot, spf)

        if parity:
            total += maxMultiplier.bit_length()

        x = maxMultiplier
        while x >= 5:
            count = oneModFourPrimeCount(x)
            for prime in excludedPrimes:
                if prime > x:
                    break
                count -= 1
            total += count
            x //= 2

    return total


def runTests():
    assert bruteOpenDoorCount(5) == 1
    assert bruteOpenDoorCount(100) == 27
    assert bruteOpenDoorCount(1_000) == 233
    assert bruteOpenDoorCount(10 ** 6) == 112_168
    assert openDoorCount(5) == 1
    assert openDoorCount(100) == 27
    assert openDoorCount(1_000) == 233
    assert openDoorCount(10 ** 6) == 112_168


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = openDoorCount(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
