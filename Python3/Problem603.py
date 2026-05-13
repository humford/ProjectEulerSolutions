import math
import time


MODULUS = 1_000_000_007
INVERSE_TWO = pow(2, -1, MODULUS)
INVERSE_NINE = pow(9, -1, MODULUS)


def primesUpToCount(count):
    if count < 6:
        limit = 20
    else:
        limit = int(count * (math.log(count) + math.log(math.log(count)))) + 100

    while True:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[0:2] = b"\x00\x00"
        for prime in range(2, math.isqrt(limit) + 1):
            if sieve[prime]:
                start = prime * prime
                sieve[start:limit + 1:prime] = (
                    b"\x00" * (((limit - start) // prime) + 1)
                )

        primes = [value for value in range(2, limit + 1) if sieve[value]]
        if len(primes) >= count:
            return primes[:count]

        limit *= 2


def substringSum(n):
    digits = str(n)
    total = 0
    for start in range(len(digits)):
        value = 0
        for end in range(start, len(digits)):
            value = 10 * value + int(digits[end])
            total += value
    return total


def primeConcatenation(n):
    return int("".join(str(prime) for prime in primesUpToCount(n)))


def blockDigitStatistics(digits):
    length = len(digits)
    weightedPowerSum = 0
    indexWeightedPowerSum = 0
    digitSum = 0
    indexWeightedDigitSum = 0
    powerOfTen = 10

    for reverseIndex, digitCharacter in enumerate(reversed(digits), 1):
        index = length - reverseIndex + 1
        digit = ord(digitCharacter) - ord("0")
        weightedPowerSum = (weightedPowerSum + digit * powerOfTen) % MODULUS
        indexWeightedPowerSum = (
            indexWeightedPowerSum
            + digit * (index % MODULUS) * powerOfTen
        ) % MODULUS
        digitSum = (digitSum + digit) % MODULUS
        indexWeightedDigitSum = (
            indexWeightedDigitSum + digit * (index % MODULUS)
        ) % MODULUS
        powerOfTen = (10 * powerOfTen) % MODULUS

    return (
        weightedPowerSum,
        indexWeightedPowerSum,
        digitSum,
        indexWeightedDigitSum,
    )


def geometricSums(ratio, count):
    countMod = count % MODULUS
    countMinusOneMod = (count - 1) % MODULUS

    if ratio == 1:
        return (
            countMod,
            countMod * countMinusOneMod * INVERSE_TWO % MODULUS,
        )

    ratioToCount = pow(ratio, count, MODULUS)
    sumPowers = (
        (ratioToCount - 1)
        * pow(ratio - 1, -1, MODULUS)
    ) % MODULUS
    sumIndexPowers = (
        (
            ratio
            - countMod * ratioToCount
            + countMinusOneMod * ratioToCount % MODULUS * ratio
        )
        * pow((1 - ratio) % MODULUS, -2, MODULUS)
    ) % MODULUS
    return sumPowers, sumIndexPowers


def repeatedPrimeSubstringSum(n, copies):
    primeBlock = "".join(str(prime) for prime in primesUpToCount(n))
    blockLength = len(primeBlock)
    (
        weightedPowerSum,
        indexWeightedPowerSum,
        digitSum,
        indexWeightedDigitSum,
    ) = blockDigitStatistics(primeBlock)

    ratio = pow(10, blockLength, MODULUS)
    sumPowers, sumIndexPowers = geometricSums(ratio, copies)
    copiesMod = copies % MODULUS
    copiesMinusOneMod = (copies - 1) % MODULUS
    blockLengthMod = blockLength % MODULUS
    triangularCopies = copiesMod * copiesMinusOneMod * INVERSE_TWO % MODULUS

    powerContribution = (
        sumPowers
        * (
            blockLengthMod
            * copiesMinusOneMod
            % MODULUS
            * weightedPowerSum
            + indexWeightedPowerSum
        )
        - blockLengthMod * sumIndexPowers % MODULUS * weightedPowerSum
    )
    plainContribution = (
        blockLengthMod * triangularCopies % MODULUS * digitSum
        + copiesMod * indexWeightedDigitSum
    )
    return (powerContribution - plainContribution) * INVERSE_NINE % MODULUS


def runTests():
    assert substringSum(2024) == 2_304
    assert primeConcatenation(7) == 2_357_111_317

    smallRepeated = int(str(primeConcatenation(7)) * 3)
    assert smallRepeated == 2_357_111_317_235_711_131_723_571_113_17
    assert repeatedPrimeSubstringSum(7, 3) == substringSum(smallRepeated) % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = repeatedPrimeSubstringSum(10 ** 6, 10 ** 12) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
