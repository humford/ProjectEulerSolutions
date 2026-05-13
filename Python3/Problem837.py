import itertools
import time


MOD = 1_234_567_891


def modularInverse(n, modulus=MOD):
    return pow(n % modulus, modulus - 2, modulus)


def batchInverses(values, modulus=MOD):
    if not values:
        return []

    prefix = [0] * len(values)
    product = 1
    for i, value in enumerate(values):
        product = product * value % modulus
        prefix[i] = product

    inverseProduct = modularInverse(prefix[-1], modulus)
    inverses = [0] * len(values)
    for i in range(len(values) - 1, -1, -1):
        previous = prefix[i - 1] if i else 1
        inverses[i] = inverseProduct * previous % modulus
        inverseProduct = inverseProduct * values[i] % modulus

    return inverses


def consecutiveInverses(start, length, modulus=MOD):
    return batchInverses(range(start, start + length), modulus)


def binomialMod(n, k, modulus=MOD, blockSize=200_000):
    if k < 0 or k > n:
        return 0

    k = min(k, n - k)
    if k == 0:
        return 1

    base = n - k
    result = 1
    start = 1

    while start <= k:
        length = min(blockSize, k - start + 1)
        inverses = consecutiveInverses(start, length, modulus)
        numerator = base + start

        for i, inverse in enumerate(inverses):
            result = result * (numerator + i) % modulus
            result = result * inverse % modulus

        start += length

    return result


def phiSixPowerCoefficient(power, degree, modulus=MOD, blockSize=200_000):
    if degree < 0 or degree > 2 * power:
        return 0

    j = degree // 3
    remainder = degree - 3 * j

    term = binomialMod(power, j, modulus, blockSize)
    if remainder == 1:
        term = term * (power % modulus) % modulus
    elif remainder == 2:
        term = term * (power % modulus) % modulus
        term = term * ((power + 1) % modulus) % modulus
        term = term * modularInverse(2, modulus) % modulus

    if remainder % 2:
        term = -term % modulus

    total = term
    currentJ = j
    currentRemainder = remainder

    while currentJ > 0:
        length = min(blockSize, currentJ)
        numerators = [0] * length
        denominators = [0] * length

        for offset in range(length):
            jValue = currentJ - offset
            rValue = currentRemainder + 3 * offset

            numerator = jValue % modulus
            numerator = numerator * ((power + rValue) % modulus) % modulus
            numerator = numerator * ((power + rValue + 1) % modulus) % modulus
            numerator = numerator * ((power + rValue + 2) % modulus) % modulus
            numerators[offset] = numerator

            denominator = (power - jValue + 1) % modulus
            denominator = denominator * ((rValue + 1) % modulus) % modulus
            denominator = denominator * ((rValue + 2) % modulus) % modulus
            denominator = denominator * ((rValue + 3) % modulus) % modulus
            denominators[offset] = denominator

        inverseDenominators = batchInverses(denominators, modulus)

        for offset in range(length):
            term = -term % modulus
            term = term * numerators[offset] % modulus
            term = term * inverseDenominators[offset] % modulus
            total += term
            if total >= modulus:
                total -= modulus

        currentJ -= length
        currentRemainder += 3 * length

    return total % modulus


def amidakujiCount(m, n, modulus=MOD):
    totalRungs = m + n
    if totalRungs % 2:
        return 0

    half = totalRungs // 2
    binomialTerm = binomialMod(totalRungs, m, modulus)
    coefficientTerm = phiSixPowerCoefficient(half, m, modulus)
    return (binomialTerm + 2 * coefficientTerm) * modularInverse(3, modulus) % modulus


def bruteAmidakujiCount(m, n):
    swaps = [0] * m + [1] * n
    count = 0

    for ordering in set(itertools.permutations(swaps)):
        state = [0, 1, 2]
        for swap in ordering:
            state[swap], state[swap + 1] = state[swap + 1], state[swap]
        if state == [0, 1, 2]:
            count += 1

    return count


def runTests():
    assert bruteAmidakujiCount(3, 3) == 2
    assert amidakujiCount(3, 3) == 2
    assert amidakujiCount(123, 321) == 172_633_303


def solve():
    return amidakujiCount(123_456_789, 987_654_321)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
