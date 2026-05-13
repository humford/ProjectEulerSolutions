from functools import lru_cache
import time


MODULUS = 123_123_123
TARGET_INDEX = 111_111_111_111_222_333


@lru_cache(None)
def is123Number(n):
    if n == 1:
        return True
    if n <= 0:
        return False

    digits = str(n)
    if any(digit not in "123" for digit in digits):
        return False

    for digit in "123":
        count = digits.count(digit)
        if count and not is123Number(count):
            return False

    return True


def factorialsUpTo(limit):
    factorials = [1] * (limit + 1)
    for i in range(1, limit + 1):
        factorials[i] = factorials[i - 1] * i
    return factorials


def allowedCountsUpTo(limit):
    return [n for n in range(1, limit + 1) if is123Number(n)]


def multinomial(factorials, total, count1, count2, count3):
    return factorials[total] // (factorials[count1] * factorials[count2] * factorials[count3])


def countValidLength(length, allowedCounts, factorials):
    possibleCounts = [0] + allowedCounts
    possibleSet = set(possibleCounts)
    total = 0

    for count1 in possibleCounts:
        for count2 in possibleCounts:
            used = count1 + count2
            if used > length:
                continue

            count3 = length - used
            if count3 in possibleSet and (count1 or count2 or count3):
                total += multinomial(factorials, length, count1, count2, count3)

    return total


def findLengthAndRank(index):
    if index <= 0:
        raise ValueError("index must be positive")

    factorials = [1]
    allowedCounts = []
    previous = 0

    for length in range(1, 5000):
        factorials.append(factorials[-1] * length)
        if is123Number(length):
            allowedCounts.append(length)

        count = countValidLength(length, allowedCounts, factorials)
        if previous + count >= index:
            return length, index - previous
        previous += count

    raise RuntimeError("length search limit exceeded")


def validTotalCounts(length, allowedCounts):
    possibleCounts = [0] + allowedCounts
    possibleSet = set(possibleCounts)
    triples = []

    for count1 in possibleCounts:
        for count2 in possibleCounts:
            used = count1 + count2
            if used > length:
                continue

            count3 = length - used
            if count3 in possibleSet and (count1 or count2 or count3):
                triples.append((count1, count2, count3))

    return triples


def countCompletions(length, factorials, triples, used1, used2, used3):
    remaining = length - used1 - used2 - used3
    total = 0

    for count1, count2, count3 in triples:
        if used1 <= count1 and used2 <= count2 and used3 <= count3:
            rest1 = count1 - used1
            rest2 = count2 - used2
            rest3 = count3 - used3
            if rest1 + rest2 + rest3 == remaining:
                total += multinomial(factorials, remaining, rest1, rest2, rest3)

    return total


def nth123String(index):
    length, rank = findLengthAndRank(index)
    factorials = factorialsUpTo(length)
    allowedCounts = allowedCountsUpTo(length)
    triples = validTotalCounts(length, allowedCounts)

    used1 = used2 = used3 = 0
    digits = []

    for _ in range(length):
        for digit in (1, 2, 3):
            next1, next2, next3 = used1, used2, used3
            if digit == 1:
                next1 += 1
            elif digit == 2:
                next2 += 1
            else:
                next3 += 1

            completions = countCompletions(length, factorials, triples, next1, next2, next3)
            if rank > completions:
                rank -= completions
            else:
                digits.append(str(digit))
                used1, used2, used3 = next1, next2, next3
                break
        else:
            raise RuntimeError("unranking failed")

    return "".join(digits)


def modDecimalString(digits, modulus):
    value = 0
    for digit in digits:
        value = (10 * value + ord(digit) - ord("0")) % modulus
    return value


def number123(index):
    return int(nth123String(index))


def runTests():
    assert number123(4) == 11
    assert number123(10) == 31
    assert number123(40) == 1_112
    assert number123(1_000) == 1_223_321
    assert number123(6_000) == 2_333_333_333_323


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = modDecimalString(nth123String(TARGET_INDEX), MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
