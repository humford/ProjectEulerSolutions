import time


MODULUS = 1_000_000_007
INVERSE_9 = pow(9, MODULUS - 2, MODULUS)
TARGET = 10_000


def combination(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def deficitSequenceCount(length, deficit):
    if deficit < 0:
        return 0
    if length == 0:
        return 1 if deficit == 0 else 0

    total = 0
    for excluded in range(deficit // 10 + 1):
        reducedDeficit = deficit - 10 * excluded
        count = (
            combination(length, excluded)
            * combination(reducedDeficit + length - 1, reducedDeficit)
        )
        total = total - count if excluded & 1 else total + count
    return total


def positiveNumberCountWithDigitSum(length, digitSum):
    deficit = 9 * length - digitSum
    if deficit < 0:
        return 0

    total = deficitSequenceCount(length, deficit)
    if deficit >= 9:
        total -= deficitSequenceCount(length - 1, deficit - 9)
    return total


def lengthAndRank(digitSum, occurrence):
    length = (digitSum + 8) // 9
    beforeLength = 0

    while True:
        count = positiveNumberCountWithDigitSum(length, digitSum)
        if beforeLength + count >= occurrence:
            return length, occurrence - beforeLength
        beforeLength += count
        length += 1


def appendRepeatedDigit(value, digit, count):
    if count <= 0:
        return value

    power = pow(10, count, MODULUS)
    if digit == 0:
        block = 0
    else:
        block = digit * (power - 1) % MODULUS
        block = block * INVERSE_9 % MODULUS
    return (value * power + block) % MODULUS


def digitSumOccurrence(digitSum, occurrence):
    length, rank = lengthAndRank(digitSum, occurrence)
    deficit = 9 * length - digitSum

    value = 0
    for digit in range(1, 10):
        usedDeficit = 9 - digit
        if usedDeficit > deficit:
            continue
        count = deficitSequenceCount(length - 1, deficit - usedDeficit)
        if rank > count:
            rank -= count
            continue

        value = digit
        length -= 1
        deficit -= usedDeficit
        break
    else:
        raise ValueError("could not choose leading digit")

    while length:
        if deficit == 0:
            return appendRepeatedDigit(value, 9, length)

        totalCount = deficitSequenceCount(length, deficit)
        ninePrefixCount = deficitSequenceCount(length - 1, deficit)

        if ninePrefixCount and rank > totalCount - ninePrefixCount:
            rankFromEnd = totalCount - rank + 1
            low = (deficit + 8) // 9
            high = length
            while low < high:
                middle = (low + high) // 2
                if deficitSequenceCount(middle, deficit) >= rankFromEnd:
                    high = middle
                else:
                    low = middle + 1

            suffixLength = low
            prefixNines = length - suffixLength
            if prefixNines:
                value = appendRepeatedDigit(value, 9, prefixNines)
                rank -= totalCount - deficitSequenceCount(suffixLength, deficit)
                length = suffixLength
                continue

        for digit in range(9):
            usedDeficit = 9 - digit
            if usedDeficit > deficit:
                continue
            count = deficitSequenceCount(length - 1, deficit - usedDeficit)
            if rank > count:
                rank -= count
                continue

            value = (value * 10 + digit) % MODULUS
            length -= 1
            deficit -= usedDeficit
            break
        else:
            value = (value * 10 + 9) % MODULUS
            length -= 1

    return value


def inverseDigitSumOccurrenceTotal(limit):
    total = 0
    for n in range(1, limit + 1):
        total += digitSumOccurrence(n ** 3, n ** 4)
        total %= MODULUS
    return total


def runTests():
    assert digitSumOccurrence(10, 1) == 19
    assert digitSumOccurrence(10, 10) == 109
    assert digitSumOccurrence(10, 100) == 1_423
    assert inverseDigitSumOccurrenceTotal(3) == 7_128
    assert inverseDigitSumOccurrenceTotal(10) == 32_287_064


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = inverseDigitSumOccurrenceTotal(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
