import time


def powersOfTen(limit):
    values = [1] * (limit + 1)
    for index in range(1, limit + 1):
        values[index] = values[index - 1] * 10
    return values


def maximumExponent(maxDigits, powers10):
    limit = powers10[maxDigits]
    exponent = 0
    value = 1
    while value <= limit:
        exponent += 1
        value *= 2
    return exponent


def digitPowerTable(maxExponent):
    table = [[0] * 10 for _ in range(maxExponent + 1)]
    for digit in range(10):
        table[1][digit] = digit
    for exponent in range(2, maxExponent + 1):
        for digit in range(10):
            table[exponent][digit] = table[exponent - 1][digit] * digit
    return table


def exponentBounds(maxDigits, maxExponent, powers10):
    lower = [0] * (maxDigits + 1)
    upper = [0] * (maxDigits + 1)
    for length in range(1, maxDigits + 1):
        lower[length] = powers10[length - 1] - 1
        upper[length] = powers10[length]

    low = [[maxExponent + 1] * 10 for _ in range(maxDigits + 1)]
    high = [[[0] * (maxDigits + 1) for _ in range(10)] for __ in range(maxDigits + 1)]

    for length in range(1, maxDigits + 1):
        for maxDigit in range(2, 10):
            power = maxDigit
            exponent = 1
            while exponent <= maxExponent and length * power < lower[length]:
                power *= maxDigit
                exponent += 1
            low[length][maxDigit] = exponent

            for maxDigitCount in range(1, length + 1):
                power = maxDigit
                best = 0
                for exponent in range(1, maxExponent + 1):
                    if maxDigitCount * power <= upper[length]:
                        best = exponent
                        power *= maxDigit
                    else:
                        break
                high[length][maxDigit][maxDigitCount] = best

    return low, high


def digitPackTables():
    pack4 = [0] * 10_000
    for value in range(10_000):
        number = value
        code = 0
        for _ in range(4):
            digit = number % 10
            code += 1 << (5 * digit)
            number //= 10
        pack4[value] = code

    exact = [[], [0] * 10, [0] * 100, [0] * 1_000, pack4]
    for length in range(1, 4):
        for value in range(10 ** length):
            number = value
            code = 0
            for _ in range(length):
                digit = number % 10
                code += 1 << (5 * digit)
                number //= 10
            exact[length][value] = code

    return pack4, exact


def packedDigits(number, length, pack4, exact):
    if length <= 4:
        return exact[length][number]
    if length <= 8:
        return pack4[number % 10_000] + exact[length - 4][number // 10_000]
    if length <= 12:
        low = number % 10_000
        number //= 10_000
        mid = number % 10_000
        high = number // 10_000
        return pack4[low] + pack4[mid] + exact[length - 8][high]

    low = number % 10_000
    number //= 10_000
    mid1 = number % 10_000
    number //= 10_000
    mid2 = number % 10_000
    high = number // 10_000
    return pack4[low] + pack4[mid1] + pack4[mid2] + exact[length - 12][high]


def nearPowerSumsByLength(maxDigits):
    powers10 = powersOfTen(maxDigits)
    maxExponent = maximumExponent(maxDigits, powers10)
    powers = digitPowerTable(maxExponent)
    lowExponent, highExponent = exponentBounds(maxDigits, maxExponent, powers10)
    pack4, exact = digitPackTables()

    results = [set() for _ in range(maxDigits + 1)]

    for length in range(1, maxDigits + 1):
        low = powers10[length - 1]
        high = powers10[length]

        for maxDigit in range(2, 10):
            maxDigitShift = 5 * maxDigit
            minExponent = lowExponent[length][maxDigit]

            for maxDigitCount in range(1, length + 1):
                firstExponent = minExponent
                lastExponent = highExponent[length][maxDigit][maxDigitCount]
                if firstExponent > lastExponent:
                    continue

                exponents = list(range(firstExponent, lastExponent + 1))
                rows = [powers[exponent] for exponent in exponents]
                baseSums = [
                    maxDigitCount * powers[exponent][maxDigit] for exponent in exponents
                ]
                remaining = length - maxDigitCount
                counts = [0] * maxDigit
                maxDigitPacked = maxDigitCount << maxDigitShift

                def checkLeaf(packedPart):
                    signature = packedPart | maxDigitPacked

                    for index, row in enumerate(rows):
                        digitPowerSum = baseSums[index]
                        for digit in range(maxDigit):
                            count = counts[digit]
                            if count:
                                digitPowerSum += count * row[digit]

                        for candidate in (digitPowerSum - 1, digitPowerSum + 1):
                            if (
                                low <= candidate < high
                                and packedDigits(candidate, length, pack4, exact) == signature
                            ):
                                results[length].add(candidate)

                def chooseCounts(digit, remainingCount, packedPart):
                    if digit == maxDigit - 1:
                        counts[digit] = remainingCount
                        checkLeaf(packedPart | (remainingCount << (5 * digit)))
                        return

                    shift = 5 * digit
                    for count in range(remainingCount + 1):
                        counts[digit] = count
                        chooseCounts(
                            digit + 1,
                            remainingCount - count,
                            packedPart | (count << shift),
                        )

                chooseCounts(0, remaining, 0)

    return results


def nearPowerSumPrefix(results, digits):
    return sum(
        number
        for length in range(1, min(digits, len(results) - 1) + 1)
        for number in results[length]
    )


def runTests(results):
    assert nearPowerSumPrefix(results, 2) == 110
    assert nearPowerSumPrefix(results, 6) == 2_562_701


if __name__ == "__main__":
    start = time.time()
    results = nearPowerSumsByLength(16)
    runTests(results)
    answer = nearPowerSumPrefix(results, 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
