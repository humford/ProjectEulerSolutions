import time
from itertools import combinations, permutations


def digitMaskInBase(number, base):
    mask = 0
    fullMask = (1 << base) - 1

    while number >= base:
        mask |= 1 << (number % base)
        if mask == fullMask:
            return mask
        number //= base

    return mask | (1 << number)


def isPandigitalInBase(number, base):
    return digitMaskInBase(number, base) == (1 << base) - 1


def isOctalPandigital(number):
    mask = 0
    for digit in oct(number)[2:]:
        mask |= 1 << (ord(digit) - ord("0"))
        if mask == 0xFF:
            return True
    return False


def isDecimalPandigital(number):
    mask = 0
    for digit in str(number):
        mask |= 1 << (ord(digit) - ord("0"))
        if mask == 0x3FF:
            return True
    return False


def isSuperPandigital(number, maxBase):
    if maxBase > 8 and not isOctalPandigital(number):
        return False

    for base in range(maxBase - 1, 1, -1):
        if base == 8 and maxBase > 8:
            continue

        if base == 10:
            isPandigital = isDecimalPandigital(number)
        else:
            isPandigital = isPandigitalInBase(number, base)

        if not isPandigital:
            return False

    return True


def digitsToNumber(digits, base):
    number = 0
    for digit in digits:
        number = number * base + digit
    return number


def digitsMask(digits):
    mask = 0
    for digit in digits:
        mask |= 1 << digit
    return mask


def tailValuesByMask(base, tailLength):
    tails = {}

    for digitSet in combinations(range(base), tailLength):
        values = [
            digitsToNumber(digits, base)
            for digits in permutations(digitSet)
        ]
        values.sort()
        tails[digitsMask(digitSet)] = values

    return tails


def superPandigitalNumbers(maxBase, resultCount):
    tailLength = maxBase // 2
    highLength = maxBase - tailLength
    fullMask = (1 << maxBase) - 1
    scale = maxBase ** tailLength
    tails = tailValuesByMask(maxBase, tailLength)
    results = []

    for highDigits in permutations(range(maxBase), highLength):
        if highDigits[0] == 0:
            continue

        prefix = digitsToNumber(highDigits, maxBase) * scale
        remainingMask = fullMask ^ digitsMask(highDigits)

        for tail in tails[remainingMask]:
            number = prefix + tail
            if isSuperPandigital(number, maxBase):
                results.append(number)
                if len(results) == resultCount:
                    return results

    raise ValueError("Not enough base-" + str(maxBase) + " pandigital results found")


def superPandigitalSum(base, resultCount=10):
    return sum(superPandigitalNumbers(base, resultCount))


def runTests():
    assert all(isPandigitalInBase(978, base) for base in range(2, 6))
    assert superPandigitalNumbers(5, 1)[0] == 978
    assert superPandigitalNumbers(10, 1)[0] == 1_093_265_784
    assert superPandigitalSum(10) == 20_319_792_309


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = superPandigitalSum(12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
