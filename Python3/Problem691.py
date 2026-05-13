import math
import time
from array import array


TARGET = 5_000_000


def inversePhiFixedPoint(bits=64):
    scale = 1 << bits
    sqrtFiveScaled = math.isqrt(5 * scale * scale)
    return (sqrtFiveScaled - scale) // 2, bits


def exactBeattyIncrement(index):
    def floorOverPhi(value):
        return (math.isqrt(5 * value * value) - value) // 2

    return floorOverPhi(index + 1) - floorOverPhi(index)


def repeatedSubstringTotal(length, returnBest=False):
    inversePhi, shift = inversePhiFixedPoint()

    nextZero = array("I", [0, 0])
    nextOne = array("I", [0, 0])
    suffixLink = array("I", [0, 0])
    maxLength = array("I", [0, 0])
    occurrences = array("I", [0, 0])

    last = 1
    stateCount = 2
    accumulator = 0
    previousFloor = 0

    for index in range(length):
        accumulator += inversePhi
        currentFloor = accumulator >> shift
        beattyDigit = currentFloor - previousFloor
        previousFloor = currentFloor
        character = (index.bit_count() & 1) ^ beattyDigit

        current = stateCount
        stateCount += 1
        nextZero.append(0)
        nextOne.append(0)
        suffixLink.append(0)
        maxLength.append(maxLength[last] + 1)
        occurrences.append(1)

        state = last
        if character == 0:
            while state and nextZero[state] == 0:
                nextZero[state] = current
                state = suffixLink[state]
            if state == 0:
                suffixLink[current] = 1
            else:
                target = nextZero[state]
                if maxLength[state] + 1 == maxLength[target]:
                    suffixLink[current] = target
                else:
                    clone = stateCount
                    stateCount += 1
                    nextZero.append(nextZero[target])
                    nextOne.append(nextOne[target])
                    suffixLink.append(suffixLink[target])
                    maxLength.append(maxLength[state] + 1)
                    occurrences.append(0)

                    while state and nextZero[state] == target:
                        nextZero[state] = clone
                        state = suffixLink[state]
                    suffixLink[target] = clone
                    suffixLink[current] = clone
        else:
            while state and nextOne[state] == 0:
                nextOne[state] = current
                state = suffixLink[state]
            if state == 0:
                suffixLink[current] = 1
            else:
                target = nextOne[state]
                if maxLength[state] + 1 == maxLength[target]:
                    suffixLink[current] = target
                else:
                    clone = stateCount
                    stateCount += 1
                    nextZero.append(nextZero[target])
                    nextOne.append(nextOne[target])
                    suffixLink.append(suffixLink[target])
                    maxLength.append(maxLength[state] + 1)
                    occurrences.append(0)

                    while state and nextOne[state] == target:
                        nextOne[state] = clone
                        state = suffixLink[state]
                    suffixLink[target] = clone
                    suffixLink[current] = clone

        last = current

    del nextZero, nextOne

    lengthCounts = array("I", [0]) * (length + 1)
    for state in range(1, stateCount):
        lengthCounts[maxLength[state]] += 1
    for substringLength in range(1, length + 1):
        lengthCounts[substringLength] += lengthCounts[substringLength - 1]

    orderedStates = array("I", [0]) * (stateCount - 1)
    for state in range(stateCount - 1, 0, -1):
        substringLength = maxLength[state]
        lengthCounts[substringLength] -= 1
        orderedStates[lengthCounts[substringLength]] = state
    del lengthCounts

    for index in range(stateCount - 2, 0, -1):
        state = orderedStates[index]
        occurrences[suffixLink[state]] += occurrences[state]
    del orderedStates

    best = array("I", [0]) * (length + 1)
    for state in range(1, stateCount):
        count = occurrences[state]
        substringLength = maxLength[state]
        if substringLength > best[count]:
            best[count] = substringLength

    for count in range(length - 1, 0, -1):
        if best[count] < best[count + 1]:
            best[count] = best[count + 1]

    total = 0
    for count in range(1, length + 1):
        value = best[count]
        if value == 0:
            break
        total += value

    if returnBest:
        return total, best
    return total


def runTests():
    total10, best10 = repeatedSubstringTotal(10, True)
    assert best10[2] == 5
    assert best10[3] == 2

    total100, best100 = repeatedSubstringTotal(100, True)
    assert best100[2] == 14
    assert best100[4] == 6

    total1000, best1000 = repeatedSubstringTotal(1_000, True)
    assert best1000[2] == 86
    assert best1000[3] == 45
    assert best1000[5] == 31
    assert total1000 == 2_460

    inversePhi, shift = inversePhiFixedPoint()
    for index in (0, 1, 2, 3, 10, 123, 10_000, 100_000, 1_000_000, 4_999_999):
        fixedIncrement = (
            ((index + 1) * inversePhi) >> shift
        ) - ((index * inversePhi) >> shift)
        assert fixedIncrement == exactBeattyIncrement(index)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = repeatedSubstringTotal(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
