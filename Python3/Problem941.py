from array import array
import sys
import time


TARGET = 10_000_000
ANSWER_MODULUS = 1_234_567_891
LCG_MODULUS = 10**12
LCG_MULTIPLIER = 920_461
LCG_INCREMENT = 800_217_387_569


def deBruijnSequence(alphabetSize, wordLength):
    state = [0] * (alphabetSize * wordLength)
    sequence = []

    def visit(t, p):
        if t > wordLength:
            if wordLength % p == 0:
                sequence.extend(state[1 : p + 1])
            return

        state[t] = state[t - p]
        visit(t + 1, p)

        for digit in range(state[t - p] + 1, alphabetSize):
            state[t] = digit
            visit(t + 1, t)

    visit(1, 1)
    base = "".join(str(digit) for digit in sequence)
    return base + base[: wordLength - 1]


def makeRankFunction(alphabetSize, wordLength):
    powers = [1] * (wordLength + 1)
    for index in range(1, wordLength + 1):
        powers[index] = powers[index - 1] * alphabetSize

    necklaceRepresentative = [0] * (wordLength + 1)
    previousNecklace = [0] * (wordLength + 1)
    temporaryNecklace = [0] * (wordLength + 1)
    B = [[0] * (wordLength + 1) for _ in range(wordLength + 1)]
    suffix = [[0] * (wordLength + 1) for _ in range(wordLength + 1)]

    def lyndonPrefixLength(word):
        period = 1
        for index in range(2, wordLength + 1):
            current = word[index]
            reference = word[index - period]
            if current < reference:
                return period
            if current > reference:
                period = index
        return period

    def isNecklace(word):
        period = 1
        for index in range(2, wordLength + 1):
            current = word[index]
            reference = word[index - period]
            if current < reference:
                return False
            if current > reference:
                period = index
        return wordLength % period == 0

    def largestNecklaceAtMost(word, out):
        for index in range(1, wordLength + 1):
            out[index] = word[index]

        while not isNecklace(out):
            period = lyndonPrefixLength(out)
            out[period] -= 1
            for index in range(period + 1, wordLength + 1):
                out[index] = alphabetSize

    def necklacePrefixCount(word):
        largestNecklaceAtMost(word, temporaryNecklace)

        B[0][0] = 1
        for t in range(1, wordLength + 1):
            row = B[t]
            row[t] = 0
            for j in range(t - 1, -1, -1):
                row[j] = (
                    row[j + 1]
                    + (alphabetSize - temporaryNecklace[j + 1]) * B[t - j - 1][0]
                )

        for i in range(2, wordLength + 1):
            start = i
            for j in range(i, wordLength + 1):
                if temporaryNecklace[j] > temporaryNecklace[j - start + 1]:
                    start = j + 1
                suffix[i][j] = j - start + 1

        total = lyndonPrefixLength(temporaryNecklace)
        for t in range(1, wordLength + 1):
            leadingCount = B[t - 1][0]
            for j in range(wordLength):
                if j + t <= wordLength:
                    total += (
                        leadingCount
                        * (temporaryNecklace[j + 1] - 1)
                        * powers[wordLength - t - j]
                    )
                else:
                    if j < wordLength - t + 2:
                        suffixLength = 0
                    else:
                        suffixLength = suffix[wordLength - t + 2][j]

                    if temporaryNecklace[j + 1] > temporaryNecklace[suffixLength + 1]:
                        total += (
                            B[wordLength - j + suffixLength][suffixLength + 1]
                            + (
                                temporaryNecklace[j + 1]
                                - temporaryNecklace[suffixLength + 1]
                                - 1
                            )
                            * B[wordLength - j - 1][0]
                        )

        return total

    def rank(word):
        leadingMaxDigits = 0
        while (
            leadingMaxDigits < wordLength
            and word[leadingMaxDigits + 1] == alphabetSize
        ):
            leadingMaxDigits += 1

        trailingOnesIndex = leadingMaxDigits
        while trailingOnesIndex < wordLength and word[trailingOnesIndex + 1] == 1:
            trailingOnesIndex += 1

        if leadingMaxDigits >= 1 and trailingOnesIndex == wordLength:
            return powers[wordLength] - leadingMaxDigits + 1

        if isNecklace(word):
            return 1 - lyndonPrefixLength(word) + necklacePrefixCount(word)

        for index in range(1, wordLength + 1):
            necklaceRepresentative[index] = word[index]

        rotation = 0
        while not isNecklace(necklaceRepresentative):
            rotation += 1
            for index in range(1, wordLength + 1):
                rotatedIndex = index + rotation
                necklaceRepresentative[index] = (
                    word[rotatedIndex]
                    if rotatedIndex <= wordLength
                    else word[rotatedIndex - wordLength]
                )

        representativeLyndonLength = lyndonPrefixLength(necklaceRepresentative)
        if rotation != leadingMaxDigits:
            return rank(necklaceRepresentative) + representativeLyndonLength - rotation

        if representativeLyndonLength < wordLength:
            return rank(necklaceRepresentative) - rotation

        for index in range(wordLength - rotation + 1, wordLength + 1):
            necklaceRepresentative[index] = 1
        largestNecklaceAtMost(necklaceRepresentative, previousNecklace)
        return rank(previousNecklace) + lyndonPrefixLength(previousNecklace) - rotation

    return rank


def makeDigitTable():
    table = [None] * 10_000
    for value in range(10_000):
        table[value] = (
            value // 1_000 + 1,
            (value // 100) % 10 + 1,
            (value // 10) % 10 + 1,
            value % 10 + 1,
        )
    return table


DIGIT_TABLE = makeDigitTable()


def writeWordSymbols(value, word):
    high = value // 100_000_000
    middle = (value // 10_000) % 10_000
    low = value % 10_000

    word[1], word[2], word[3], word[4] = DIGIT_TABLE[high]
    word[5], word[6], word[7], word[8] = DIGIT_TABLE[middle]
    word[9], word[10], word[11], word[12] = DIGIT_TABLE[low]


def generatedValues(limit):
    value = 0
    for _ in range(limit):
        value = (LCG_MULTIPLIER * value + LCG_INCREMENT) % LCG_MODULUS
        yield value


def radixSortPairs(keys, values):
    length = len(keys)
    if length <= 1:
        return

    bitsPerPass = 16
    radix = 1 << bitsPerPass
    mask = radix - 1
    temporaryKeys = array("Q", [0]) * length
    temporaryValues = array("Q", [0]) * length
    sourceKeys = keys
    sourceValues = values
    targetKeys = temporaryKeys
    targetValues = temporaryValues

    for shift in (0, 16, 32):
        counts = [0] * radix

        for key in sourceKeys:
            counts[(key >> shift) & mask] += 1

        total = 0
        for bucket in range(radix):
            count = counts[bucket]
            counts[bucket] = total
            total += count

        for index in range(length):
            key = sourceKeys[index]
            bucket = (key >> shift) & mask
            targetIndex = counts[bucket]
            targetKeys[targetIndex] = key
            targetValues[targetIndex] = sourceValues[index]
            counts[bucket] = targetIndex + 1

        sourceKeys, targetKeys = targetKeys, sourceKeys
        sourceValues, targetValues = targetValues, sourceValues

    if sourceKeys is not keys:
        keys[:] = sourceKeys
        values[:] = sourceValues


def F(limit, modulus=None):
    if modulus is None:
        modulus = 2**63 - 1

    rank = makeRankFunction(10, 12)
    word = [0] * 13
    ranks = array("Q")
    values = array("Q")
    appendRank = ranks.append
    appendValue = values.append

    for value in generatedValues(limit):
        writeWordSymbols(value, word)
        appendRank(rank(word))
        appendValue(value)

    radixSortPairs(ranks, values)

    total = 0
    for index, value in enumerate(values, 1):
        total = (total + index * (value % modulus)) % modulus

    return total


def solve():
    return F(TARGET, ANSWER_MODULUS)


def runTests():
    assert deBruijnSequence(3, 2) == "0010211220"

    testRank = makeRankFunction(2, 4)
    sequence = deBruijnSequence(2, 4)
    for number in range(2**4):
        bits = format(number, "04b")
        word = [0] * 5
        for index, bit in enumerate(bits, 1):
            word[index] = int(bit) + 1
        assert testRank(word) == sequence.find(bits) + 1

    assert F(2) == 2_194_210_461_325
    assert F(10) == 32_698_850_376_317


if __name__ == "__main__":
    runTests()
    target = TARGET
    if len(sys.argv) > 1:
        target = int(sys.argv[1])

    start = time.time()
    answer = F(target, ANSWER_MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
