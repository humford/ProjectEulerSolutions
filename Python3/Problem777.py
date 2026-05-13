import time


def dNumeratorOver4(a, b):
    product = a * b
    if product % 10 == 0:
        return 2 * product - 3 * a - 3 * b + 4
    return 8 * product - 6 * a - 6 * b


def firstSum(n):
    return n * (n + 1) // 2


def mobiusSieve(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    primes = []
    isComposite = bytearray(limit + 1)

    for n in range(2, limit + 1):
        if not isComposite[n]:
            primes.append(n)
            mu[n] = -1
        for prime in primes:
            value = n * prime
            if value > limit:
                break
            isComposite[value] = 1
            if n % prime == 0:
                mu[value] = 0
                break
            mu[value] = -mu[n]

    return mu


def specialPairSums(n, needFactor2, needFactor5):
    totalCount = n * n
    totalSum = firstSum(n)
    totalSumX = totalSum * n
    totalSumXY = totalSum * totalSum

    if not needFactor2 and not needFactor5:
        return totalCount, totalSumX, totalSumXY

    evenCount = n // 2
    evenSum = 2 * firstSum(evenCount)
    oddCount = n - evenCount
    oddSum = totalSum - evenSum

    multiple5Count = n // 5
    multiple5Sum = 5 * firstSum(multiple5Count)
    not5Count = n - multiple5Count
    not5Sum = totalSum - multiple5Sum

    multiple10Count = n // 10
    multiple10Sum = 10 * firstSum(multiple10Count)
    oddNot5Count = n - evenCount - multiple5Count + multiple10Count
    oddNot5Sum = totalSum - evenSum - multiple5Sum + multiple10Sum

    if needFactor2 and not needFactor5:
        return (
            totalCount - oddCount * oddCount,
            totalSumX - oddSum * oddCount,
            totalSumXY - oddSum * oddSum,
        )

    if needFactor5 and not needFactor2:
        return (
            totalCount - not5Count * not5Count,
            totalSumX - not5Sum * not5Count,
            totalSumXY - not5Sum * not5Sum,
        )

    return (
        totalCount - oddCount * oddCount - not5Count * not5Count + oddNot5Count * oddNot5Count,
        totalSumX - oddSum * oddCount - not5Sum * not5Count + oddNot5Sum * oddNot5Count,
        totalSumXY - oddSum * oddSum - not5Sum * not5Sum + oddNot5Sum * oddNot5Sum,
    )


def sNumeratorOver4(limit):
    mu = mobiusSieve(limit)
    sumAB = 0
    sumA = 0
    specialCount = 0
    specialSumA = 0
    specialSumAB = 0

    for divisor in range(1, limit + 1):
        mobius = mu[divisor]
        if mobius == 0:
            continue
        n = limit // divisor
        S = firstSum(n)

        sumAB += mobius * divisor * divisor * S * S
        sumA += mobius * divisor * S * n

        needFactor2 = divisor % 2 == 1
        needFactor5 = divisor % 5 != 0
        count, localSumX, localSumXY = specialPairSums(n, needFactor2, needFactor5)
        specialCount += mobius * count
        specialSumA += mobius * divisor * localSumX
        specialSumAB += mobius * divisor * divisor * localSumXY

    totalFirstSum = firstSum(limit)
    # Restrict from [1..m]^2 to [2..m]^2.
    sumAB = sumAB - 2 * totalFirstSum + 1
    sumA = sumA - limit - totalFirstSum + 1

    multiples10Count = limit // 10
    multiples10Sum = 10 * firstSum(multiples10Count)
    specialCount -= 2 * multiples10Count
    specialSumA -= multiples10Count + multiples10Sum
    specialSumAB -= 2 * multiples10Sum

    generic = 8 * sumAB - 12 * sumA
    specialCorrection = -6 * specialSumAB + 6 * specialSumA + 4 * specialCount
    return generic + specialCorrection


def roundDivision(numerator, denominator):
    return (2 * numerator + denominator) // (2 * denominator)


def formatScientific(numerator, denominator=1, significantDigits=10):
    integerPart = numerator // denominator
    exponent = len(str(integerPart)) - 1 if integerPart else 0
    power = significantDigits - 1 - exponent
    if power >= 0:
        scaled = roundDivision(numerator * (10 ** power), denominator)
    else:
        scaled = roundDivision(numerator, denominator * (10 ** (-power)))

    if scaled >= 10 ** significantDigits:
        scaled //= 10
        exponent += 1

    digits = str(scaled).zfill(significantDigits)
    return digits[0] + "." + digits[1:] + "e" + str(exponent)


def runTests():
    assert dNumeratorOver4(2, 5) == 3
    assert dNumeratorOver4(2, 3) == 18
    assert dNumeratorOver4(7, 4) == 158
    assert dNumeratorOver4(7, 5) == 208
    assert dNumeratorOver4(10, 7) == 93
    assert sNumeratorOver4(10) == 6_410
    assert sNumeratorOver4(100) == 97_026_020


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formatScientific(sNumeratorOver4(10 ** 6), 4)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
