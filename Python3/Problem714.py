from collections import deque
import math
import time


def isDuodigit(number):
    first = None
    second = None

    for digit in str(number):
        if first is None:
            first = digit
        elif digit != first:
            if second is None:
                second = digit
            elif digit != second:
                return False

    return True


def generateDuodigits(maxLength):
    result = []

    for length in range(1, maxLength + 1):
        for digit in range(1, 10):
            result.append(int(str(digit) * length))

        for a in range(0, 9):
            for b in range(a + 1, 10):
                if a == 0:
                    if length == 1:
                        continue

                    topBit = 1 << (length - 1)
                    limit = 1 << (length - 1)
                    for tail in range(limit):
                        if tail == limit - 1:
                            continue

                        mask = topBit | tail
                        number = 0
                        for position in range(length - 1, -1, -1):
                            number = 10 * number + (b if (mask >> position) & 1 else 0)
                        result.append(number)
                else:
                    limit = 1 << length
                    for mask in range(1, limit - 1):
                        number = 0
                        for position in range(length - 1, -1, -1):
                            number = 10 * number + (b if (mask >> position) & 1 else a)
                        result.append(number)

    result.sort()
    return result


def formatScientific13(number):
    digits = str(number)
    exponent = len(digits) - 1
    significant = 13

    if len(digits) <= significant:
        kept = digits.ljust(significant, "0")
    else:
        kept = digits[:significant]
        if ord(digits[significant]) - ord("0") >= 5:
            keptList = list(kept)
            i = significant - 1
            while i >= 0:
                if keptList[i] != "9":
                    keptList[i] = chr(ord(keptList[i]) + 1)
                    break
                keptList[i] = "0"
                i -= 1

            if i < 0:
                exponent += 1
                kept = "1" + "0" * (significant - 1)
            else:
                kept = "".join(keptList)

    return kept[0] + "." + kept[1:] + "e" + str(exponent)


def smallestMultiple01(modulus):
    if modulus == 1:
        return "1"

    previous = [-1] * modulus
    previousDigit = [-1] * modulus
    start = 1 % modulus
    queue = deque([start])
    previous[start] = -2
    previousDigit[start] = 1

    while queue:
        remainder = queue.popleft()
        if remainder == 0:
            break

        shifted = (10 * remainder) % modulus
        for digit in (0, 1):
            nextRemainder = (shifted + digit) % modulus
            if previous[nextRemainder] == -1:
                previous[nextRemainder] = remainder
                previousDigit[nextRemainder] = digit
                queue.append(nextRemainder)

    remainder = 0
    digits = []
    while True:
        digits.append(str(previousDigit[remainder]))
        parent = previous[remainder]
        if parent == -2:
            break
        remainder = parent

    return "".join(reversed(digits))


def bestZeroDigitMultiple(base, cache01):
    best = None

    for digit in range(1, 10):
        reduced = base // math.gcd(base, digit)
        pattern = cache01[reduced]
        candidate = "".join("0" if ch == "0" else str(digit) for ch in pattern)
        if best is None or (len(candidate), candidate) < (len(best), best):
            best = candidate

    return best


def bfsDuodigitMultiple(number):
    goodMask = [False] * 1024
    for mask in range(1, 1024):
        bits = mask.bit_count()
        if bits <= 2:
            goodMask[mask] = True

    def key(mask, remainder):
        return mask * number + remainder

    queue = deque()
    parent = {}
    digitOf = {}

    for digit in range(1, 10):
        mask = 1 << digit
        remainder = digit % number
        state = key(mask, remainder)
        if state not in parent:
            parent[state] = -1
            digitOf[state] = digit
            queue.append((mask, remainder))
        if remainder == 0:
            return digit

    while queue:
        mask, remainder = queue.popleft()
        for digit in range(10):
            nextMask = mask | (1 << digit)
            if not goodMask[nextMask]:
                continue

            nextRemainder = (10 * remainder + digit) % number
            state = key(nextMask, nextRemainder)
            if state in parent:
                continue

            parent[state] = key(mask, remainder)
            digitOf[state] = digit
            if nextRemainder == 0:
                digits = []
                current = state
                while current != -1:
                    digits.append(str(digitOf[current]))
                    current = parent[current]
                return int("".join(reversed(digits)))
            queue.append((nextMask, nextRemainder))

    raise RuntimeError("every number should have a duodigit multiple")


def computeDuodigitValues(limit):
    candidates = generateDuodigits(15)
    cache01 = [""] * (limit // 10 + 1)
    for modulus in range(1, len(cache01)):
        cache01[modulus] = smallestMultiple01(modulus)

    values = [0] * (limit + 1)
    for number in range(1, limit + 1):
        if number % 10 == 0:
            values[number] = int(bestZeroDigitMultiple(number // 10, cache01) + "0")
        elif isDuodigit(number):
            values[number] = number
        else:
            found = None
            for candidate in candidates:
                if candidate % number == 0:
                    found = candidate
                    break
            if found is None:
                found = bfsDuodigitMultiple(number)
            values[number] = found

    return values


def smallestDuodigitMultiple(number):
    if isDuodigit(number):
        return number
    return bfsDuodigitMultiple(number)


def duodigitMultipleSum(limit):
    values = computeDuodigitValues(limit)
    return sum(values[1:])


def runTests():
    assert isDuodigit(12)
    assert isDuodigit(110)
    assert isDuodigit(33_333)
    assert not isDuodigit(102)
    assert smallestDuodigitMultiple(12) == 12
    assert smallestDuodigitMultiple(102) == 1_122
    assert smallestDuodigitMultiple(103) == 515
    assert smallestDuodigitMultiple(290) == 11_011_010
    assert smallestDuodigitMultiple(317) == 211_122

    values = computeDuodigitValues(500)
    prefix = 0
    sums = {}
    for number in range(1, 501):
        prefix += values[number]
        if number in (110, 150, 500):
            sums[number] = prefix
    assert sums[110] == 11_047
    assert sums[150] == 53_312
    assert sums[500] == 29_570_988


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formatScientific13(duodigitMultipleSum(50_000))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
