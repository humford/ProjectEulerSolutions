from bisect import bisect_left
import time


TARGET_N = 20
TARGET_K = 7
MODULUS = 1_001_001_011


def ceilDivPowerOfTwo(value, shift):
    if shift == 0:
        return value

    divisor = 1 << shift
    if value >= 0:
        return (value + divisor - 1) >> shift
    return -((-value) >> shift)


def simplestDyadicBetween(lower, upper, exponent):
    for mantissaBits in range(exponent + 1):
        shift = exponent - mantissaBits
        minMantissa = (lower >> shift) + 1
        maxMantissa = ceilDivPowerOfTwo(upper, shift) - 1

        if minMantissa <= maxMantissa:
            if minMantissa > 0:
                mantissa = minMantissa
            elif maxMantissa < 0:
                mantissa = maxMantissa
            else:
                mantissa = 0

            if mantissaBits > 0 and mantissa and mantissa % 2 == 0:
                if mantissa + 1 <= maxMantissa and (mantissa + 1) % 2:
                    mantissa += 1
                elif mantissa - 1 >= minMantissa and (mantissa - 1) % 2:
                    mantissa -= 1

            return mantissa << shift

    return 0


def computeWordValues(length):
    scale = 1 << length
    totalWords = (1 << (length + 1)) - 1
    leftStop = [0] * totalWords
    rightStop = [0] * totalWords

    firstLengthStart = 1
    rightWord = firstLengthStart
    leftWord = firstLengthStart + 1
    leftStop[rightWord] = rightStop[rightWord] = -scale
    leftStop[leftWord] = rightStop[leftWord] = scale

    hot = [0] * (1 << length)
    for wordLength in range(2, length + 1):
        start = (1 << wordLength) - 1

        for bits in range(1 << wordLength):
            leftRaw = -(2**31)
            for suffixLength in range(1, wordLength):
                suffix = bits & ((1 << suffixLength) - 1)
                index = ((1 << suffixLength) - 1) + suffix
                leftRaw = max(leftRaw, rightStop[index])

            rightRaw = 2**31 - 1
            for prefixLength in range(1, wordLength):
                prefix = bits >> (wordLength - prefixLength)
                index = ((1 << prefixLength) - 1) + prefix
                rightRaw = min(rightRaw, leftStop[index])

            index = start + bits
            if leftRaw < rightRaw:
                value = simplestDyadicBetween(leftRaw, rightRaw, length)
                leftStop[index] = value
                rightStop[index] = value
            else:
                leftStop[index] = leftRaw
                rightStop[index] = rightRaw
                if wordLength == length:
                    hot[bits] = 1

    targetStart = (1 << length) - 1
    return leftStop[targetStart : targetStart + (1 << length)], hot


def histogram(values, modulus):
    counts = {}
    for value in values:
        counts[value] = (counts.get(value, 0) + 1) % modulus
    return {value: count for value, count in counts.items() if count}


def convolve(left, right, modulus):
    if len(left) > len(right):
        left, right = right, left

    result = {}
    for leftValue, leftCount in left.items():
        for rightValue, rightCount in right.items():
            value = leftValue + rightValue
            result[value] = (
                result.get(value, 0) + leftCount * rightCount
            ) % modulus
    return {value: count for value, count in result.items() if count}


def histogramPower(hist, exponent, modulus):
    if exponent == 0:
        return {0: 1}

    result = dict(hist)
    for _ in range(1, exponent):
        result = convolve(result, hist, modulus)
    return result


def countSumLessThanZero(left, right, modulus):
    rightItems = sorted(right.items())
    rightValues = [value for value, _ in rightItems]
    prefix = [0]
    running = 0

    for _, count in rightItems:
        running = (running + count) % modulus
        prefix.append(running)

    total = 0
    for leftValue, leftCount in left.items():
        index = bisect_left(rightValues, -leftValue)
        total = (total + leftCount * prefix[index]) % modulus
    return total


def countSumEqualZero(left, right, modulus):
    if len(left) > len(right):
        left, right = right, left

    total = 0
    for value, count in left.items():
        total = (total + count * right.get(-value, 0)) % modulus
    return total


def G(length, wordCount, modulus=MODULUS):
    if wordCount % 2 == 0:
        raise ValueError("wordCount must be odd")

    values, hot = computeWordValues(length)
    allHistogram = histogram(values, modulus)
    coldHistogram = histogram(
        [value for value, isHot in zip(values, hot) if not isHot], modulus
    )

    leftGroupSize = wordCount // 2
    rightGroupSize = wordCount - leftGroupSize
    allLeft = histogramPower(allHistogram, leftGroupSize, modulus)
    allRight = histogramPower(allHistogram, rightGroupSize, modulus)
    negative = countSumLessThanZero(allLeft, allRight, modulus)

    coldLeft = histogramPower(coldHistogram, leftGroupSize, modulus)
    coldRight = histogramPower(coldHistogram, rightGroupSize, modulus)
    coldZero = countSumEqualZero(coldLeft, coldRight, modulus)

    return (negative + coldZero) % modulus


def runTests():
    assert G(2, 3, 2**64) == 14
    assert G(4, 3, 2**64) == 496
    assert G(8, 5, 2**64) == 26_359_197_010


def solve():
    return G(TARGET_N, TARGET_K, MODULUS)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
