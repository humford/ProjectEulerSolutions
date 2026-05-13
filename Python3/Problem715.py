from math import isqrt
import time


MODULUS = 1_000_000_007


def characterMod4(n):
    if n % 2 == 0:
        return 0
    return 1 if n % 4 == 1 else -1


def sumCubes(n):
    triangle = n * (n + 1) // 2
    return triangle * triangle % MODULUS


def prefixCharacter(n):
    if n <= 0:
        return 0
    return 1 if n % 4 in (1, 2) else 0


def sievePrimes(limit):
    if limit < 2:
        return []

    size = limit // 2 + 1
    sieve = bytearray(b"\x01") * size
    sieve[0] = 0
    root = isqrt(limit)

    for i in range(1, root // 2 + 1):
        if sieve[i]:
            prime = 2 * i + 1
            start = prime * prime // 2
            sieve[start::prime] = b"\x00" * (((size - 1 - start) // prime) + 1)

    primes = [2]
    primes.extend(2 * i + 1 for i in range(1, size) if sieve[i])
    return primes


def buildValuesAndIndex(limit):
    root = isqrt(limit)
    large = []
    i = 1
    while i <= limit:
        value = limit // i
        large.append(value)
        i = limit // value + 1

    small = list(range(root, 0, -1))
    values = []
    i = j = 0

    while i < len(large) and j < len(small):
        if large[i] > small[j]:
            values.append(large[i])
            i += 1
        elif large[i] < small[j]:
            values.append(small[j])
            j += 1
        else:
            values.append(large[i])
            i += 1
            j += 1

    values.extend(large[i:])
    values.extend(small[j:])

    indexSmall = [0] * (root + 1)
    indexLarge = [0] * (root + 1)
    for index, value in enumerate(values):
        if value <= root:
            indexSmall[value] = index
        else:
            indexLarge[limit // value] = index

    return values, root, indexSmall, indexLarge


def computePrimeSums(limit, primes):
    values, root, indexSmall, indexLarge = buildValuesAndIndex(limit)
    cubeSums = [0] * len(values)
    characterSums = [0] * len(values)

    for i, value in enumerate(values):
        cubeSums[i] = (sumCubes(value) - 1) % MODULUS
        characterSums[i] = (prefixCharacter(value) - 1) % MODULUS

    active = len(values)
    for prime in primes:
        primeSquared = prime * prime
        if primeSquared > limit:
            break

        while active > 0 and values[active - 1] < primeSquared:
            active -= 1

        primeMinusOneIndex = indexSmall[prime - 1]
        cubeBeforePrime = cubeSums[primeMinusOneIndex]
        characterBeforePrime = characterSums[primeMinusOneIndex]
        primeCube = prime * prime % MODULUS * prime % MODULUS
        primeCharacter = characterMod4(prime)

        for i in range(active):
            value = values[i]
            quotient = value // prime
            quotientIndex = indexSmall[quotient] if quotient <= root else indexLarge[limit // quotient]
            cubeSums[i] = (cubeSums[i] - primeCube * ((cubeSums[quotientIndex] - cubeBeforePrime) % MODULUS)) % MODULUS
            if primeCharacter:
                characterSums[i] = (
                    characterSums[i]
                    - primeCharacter * ((characterSums[quotientIndex] - characterBeforePrime) % MODULUS)
                ) % MODULUS

    primeSums = [(cubeSums[i] - characterSums[i]) % MODULUS for i in range(len(values))]
    return root, indexSmall, indexLarge, primeSums


def sextupletNormSum(limit):
    root = isqrt(limit)
    primes = sievePrimes(root)
    root, indexSmall, indexLarge, primeSums = computePrimeSums(limit, primes)
    primeCount = len(primes)
    keyBase = primeCount + 1
    memo = {}

    def indexOf(x):
        if x <= root:
            return indexSmall[x]
        return indexLarge[limit // x]

    def primeSumUpTo(x):
        if x < 2:
            return 0
        return primeSums[indexOf(x)]

    def primeSumRange(low, high):
        if high <= low:
            return 0
        return (primeSumUpTo(high) - primeSumUpTo(low)) % MODULUS

    def summatory(n, primeIndex):
        if n < 2:
            return 1

        if primeIndex >= primeCount:
            return (1 + primeSumRange(primes[-1], n)) % MODULUS

        prime = primes[primeIndex]
        if prime > n:
            return 1

        key = n * keyBase + primeIndex
        if key in memo:
            return memo[key]

        lowerPrime = primes[primeIndex - 1] if primeIndex > 0 else 1
        if prime * prime > n:
            result = (1 + primeSumRange(lowerPrime, n)) % MODULUS
            memo[key] = result
            return result

        result = (1 + primeSumRange(lowerPrime, n)) % MODULUS

        for j in range(primeIndex, primeCount):
            p = primes[j]
            p2 = p * p
            if p2 > n:
                break

            p3 = p * p % MODULUS * p % MODULUS
            sign = characterMod4(p)
            primeValue = (p3 - sign) % MODULUS
            result = (result + primeValue * ((summatory(n // p, j + 1) - 1) % MODULUS)) % MODULUS

            previousPowerValue = p3
            currentPowerValue = previousPowerValue * p3 % MODULUS
            primePower = p2

            while primePower <= n:
                gValue = (currentPowerValue - sign * previousPowerValue) % MODULUS
                result = (result + gValue * summatory(n // primePower, j + 1)) % MODULUS

                if primePower > n // p:
                    break
                primePower *= p
                previousPowerValue, currentPowerValue = currentPowerValue, currentPowerValue * p3 % MODULUS

        memo[key] = result
        return result

    return summatory(limit, 0) % MODULUS


def runTests():
    assert sextupletNormSum(10) == 3_053
    assert sextupletNormSum(10 ** 5) == 157_612_967


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sextupletNormSum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
