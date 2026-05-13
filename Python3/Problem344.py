import math
import time
from array import array


LIMIT = 1_000_000
COINS = 100
MODULUS = 1_000_036_000_099
PRIME_1 = 1_000_003
PRIME_2 = 1_000_033


def evenChooseCoefficients(count, modulus):
    return [math.comb(count, 2 * index) % modulus for index in range(count // 2 + 1)]


def xorZeroCountsBySum(count, maxSum, modulus):
    coefficients = evenChooseCoefficients(count, modulus)

    def recurse(limit):
        if limit == 0:
            return array("Q", [1])

        previous = recurse(limit // 2)
        values = array("Q", [0]) * (limit + 1)

        for total in range(limit // 2 + 1):
            subtotal = 0
            maxIndex = min(count // 2, total)

            for index in range(maxIndex + 1):
                subtotal += coefficients[index] * previous[total - index]

            values[2 * total] = subtotal % modulus

        return values

    return recurse(maxSum)


def reduceArray(values, modulus):
    reduced = array("I", [0]) * len(values)

    for index, value in enumerate(values):
        reduced[index] = value % modulus

    return reduced


def nCkModPrimeSmallK(n, k, prime):
    if k < 0 or k > n:
        return 0

    k = min(k, n - k)
    numerator = 1
    denominator = 1
    base = n - k

    for index in range(1, k + 1):
        numerator = numerator * (base + index) % prime
        denominator = denominator * index % prime

    return numerator * pow(denominator, prime - 2, prime) % prime


def inverseTable(prime, maxValue):
    inverses = array("I", [0]) * (maxValue + 1)
    inverses[1] = 1

    for value in range(2, maxValue + 1):
        inverses[value] = (
            prime - (prime // value) * inverses[prime % value] % prime
        ) % prime

    return inverses


def winningConfigurationsExact(stripLength, worthlessCoins):
    half = worthlessCoins // 2
    coinCount = worthlessCoins + 1
    emptySquares = stripLength - coinCount
    evenGapCount = half + 1

    def exactXorZeroCounts(count, maxSum):
        coefficients = [math.comb(count, 2 * index) for index in range(count // 2 + 1)]

        def recurse(limit):
            if limit == 0:
                return [1]

            previous = recurse(limit // 2)
            values = [0] * (limit + 1)

            for total in range(limit // 2 + 1):
                subtotal = 0

                for index in range(min(count // 2, total) + 1):
                    subtotal += coefficients[index] * previous[total - index]

                values[2 * total] = subtotal

            return values

        return recurse(maxSum)

    countsEven = exactXorZeroCounts(evenGapCount, emptySquares + 1)
    countsHalf = exactXorZeroCounts(half, emptySquares + 1)

    losingSecondCoin = 0
    losingOtherCoins = 0

    for gapSum in range(emptySquares + 1):
        weight = math.comb(emptySquares - gapSum + half, half)
        losingSecondCoin += countsEven[gapSum] * weight
        losingOtherCoins += (countsEven[gapSum + 1] - countsHalf[gapSum + 1]) * weight

    total = coinCount * math.comb(stripLength, coinCount)
    losing = losingSecondCoin + (worthlessCoins - 1) * losingOtherCoins
    return total - losing


def winningConfigurationsMod(stripLength=LIMIT, worthlessCoins=COINS):
    half = worthlessCoins // 2
    coinCount = worthlessCoins + 1
    emptySquares = stripLength - coinCount
    evenGapCount = half + 1

    countsEvenMod = xorZeroCountsBySum(evenGapCount, emptySquares + 1, MODULUS)
    countsHalfMod = xorZeroCountsBySum(half, emptySquares + 1, MODULUS)

    countsEven1 = reduceArray(countsEvenMod, PRIME_1)
    countsHalf1 = reduceArray(countsHalfMod, PRIME_1)
    countsEven2 = reduceArray(countsEvenMod, PRIME_2)
    countsHalf2 = reduceArray(countsHalfMod, PRIME_2)

    def solvePrime(prime, countsEven, countsHalf):
        inverses = inverseTable(prime, emptySquares + half)
        topEven = emptySquares + half
        weightEven = nCkModPrimeSmallK(topEven, half, prime)
        weightOdd = weightEven * (topEven - half) % prime * inverses[topEven] % prime

        losingSecondCoin = 0
        losingOtherCoins = 0
        currentEvenTop = topEven
        currentOddTop = topEven - 1

        for index in range(emptySquares // 2 + 1):
            evenSum = 2 * index
            losingSecondCoin = (
                losingSecondCoin + countsEven[evenSum] * weightEven
            ) % prime

            if evenSum + 1 <= emptySquares:
                diff = (countsEven[evenSum + 2] - countsHalf[evenSum + 2]) % prime
                losingOtherCoins = (losingOtherCoins + diff * weightOdd) % prime

            if index != emptySquares // 2:
                weightEven = (
                    weightEven
                    * (currentEvenTop - half)
                    * (currentEvenTop - half - 1)
                    * inverses[currentEvenTop]
                    * inverses[currentEvenTop - 1]
                ) % prime
                currentEvenTop -= 2

                weightOdd = (
                    weightOdd
                    * (currentOddTop - half)
                    * (currentOddTop - half - 1)
                    * inverses[currentOddTop]
                    * inverses[currentOddTop - 1]
                ) % prime
                currentOddTop -= 2

        total = coinCount * nCkModPrimeSmallK(stripLength, coinCount, prime) % prime
        losing = (losingSecondCoin + (worthlessCoins - 1) * losingOtherCoins) % prime

        return (total - losing) % prime

    residue1 = solvePrime(PRIME_1, countsEven1, countsHalf1)
    residue2 = solvePrime(PRIME_2, countsEven2, countsHalf2)
    adjustment = ((residue2 - residue1) % PRIME_2) * pow(PRIME_1, -1, PRIME_2)
    adjustment %= PRIME_2

    return (residue1 + PRIME_1 * adjustment) % MODULUS


def runTests():
    assert winningConfigurationsExact(10, 2) == 324
    assert winningConfigurationsExact(100, 10) == 1514704946113500


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = winningConfigurationsMod()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
