import time


MODULUS = 1_000_000_007
TARGET_N = 10**16


def nextPermutationDigits(digits):
    pivot = len(digits) - 2

    while pivot >= 0 and digits[pivot] >= digits[pivot + 1]:
        pivot -= 1

    if pivot < 0:
        return False

    swapIndex = len(digits) - 1
    while digits[swapIndex] <= digits[pivot]:
        swapIndex -= 1

    digits[pivot], digits[swapIndex] = digits[swapIndex], digits[pivot]
    digits[pivot + 1:] = reversed(digits[pivot + 1:])

    return True


def digitsToInteger(digits):
    value = 0
    for digit in digits:
        value = 10 * value + digit
    return value


def B(n):
    digits = [int(digit) for digit in str(n)]
    if not nextPermutationDigits(digits):
        return 0
    return digitsToInteger(digits)


def bruteT(n):
    return sum(B(i * i) for i in range(1, n + 1)) % MODULUS


def sumSquares(n):
    if n <= 0:
        return 0

    a = n % MODULUS
    b = (n + 1) % MODULUS
    c = (2 * n + 1) % MODULUS

    return a * b % MODULUS * c % MODULUS * pow(6, MODULUS - 2, MODULUS) % MODULUS


def suffixDigitsLow(value, length):
    digits = []
    for _ in range(length):
        value, digit = divmod(value, 10)
        digits.append(digit)
    return digits


def deltaFromKnownSuffix(digitsLow, suffixValue):
    hasAscent = False
    previous = -1

    for digit in digitsLow:
        if previous > digit:
            hasAscent = True
            break
        previous = digit

    if not hasAscent:
        return None

    digits = digitsLow[::-1]
    nextPermutationDigits(digits)
    return digitsToInteger(digits) - suffixValue


def squarePermutationDelta(n):
    square = n * n
    return B(square) - square


def sumDeltaForLength(length, powersOfTen, powersOfTenMod):
    total = 0
    stack = []

    for firstDigit in range(10):
        if length == 1 and firstDigit == 0:
            continue
        trailingZeros = 1 if firstDigit == 0 else 0
        stack.append((1, firstDigit, trailingZeros))

    while stack:
        knownDigits, suffixValue, trailingZeros = stack.pop()
        knownSquareDigits = knownDigits + trailingZeros
        squareSuffix = (suffixValue * suffixValue) % powersOfTen[knownSquareDigits]
        digitsLow = suffixDigitsLow(squareSuffix, knownSquareDigits)
        delta = deltaFromKnownSuffix(digitsLow, squareSuffix)

        if delta is not None:
            if knownDigits < length:
                completionCount = 9 * powersOfTenMod[length - knownDigits - 1] % MODULUS
                total = (total + delta * completionCount) % MODULUS
            else:
                total = (total + delta) % MODULUS
            continue

        if knownDigits == length:
            total = (total + squarePermutationDelta(suffixValue)) % MODULUS
            continue

        addingMostSignificantDigit = knownDigits + 1 == length
        digitStart = 1 if addingMostSignificantDigit else 0
        for digit in range(9, digitStart - 1, -1):
            nextSuffix = suffixValue + digit * powersOfTen[knownDigits]
            nextTrailingZeros = trailingZeros
            if trailingZeros == knownDigits and digit == 0:
                nextTrailingZeros = knownDigits + 1
            stack.append((knownDigits + 1, nextSuffix, nextTrailingZeros))

    return total % MODULUS


def T(n):
    # A power-of-ten endpoint contributes zero: its square is 1 followed by
    # zeros, which has no larger digit permutation.
    if str(n)[0] == "1" and set(str(n)[1:]) <= {"0"}:
        n -= 1

    maxLength = len(str(n))
    powersOfTen = [1]
    for _ in range(2 * maxLength + 1):
        powersOfTen.append(10 * powersOfTen[-1])

    powersOfTenMod = [1]
    for _ in range(maxLength + 1):
        powersOfTenMod.append(10 * powersOfTenMod[-1] % MODULUS)

    deltaSum = 0
    for length in range(1, maxLength + 1):
        deltaSum = (
            deltaSum + sumDeltaForLength(length, powersOfTen, powersOfTenMod)
        ) % MODULUS

    return (sumSquares(n) + deltaSum) % MODULUS


def solve():
    return T(TARGET_N)


def runTests():
    assert B(245) == 254
    assert B(542) == 0
    assert bruteT(10) == 270
    assert bruteT(100) == 335_316
    assert T(10) == 270
    assert T(100) == 335_316


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
