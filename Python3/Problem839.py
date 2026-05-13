from array import array
import time


MOD = 50_515_093
SEED = 290_797


def unsignedLongLongArray():
    try:
        return array("Q")
    except ValueError:
        return array("L")


def B(bowls):
    if bowls <= 1:
        return 0

    lengths = array("I")
    totals = unsignedLongLongArray()
    value = SEED
    initialPotential = 0

    for index in range(bowls):
        initialPotential += index * value
        lengths.append(1)
        totals.append(value)

        while len(lengths) >= 2:
            leftLength = lengths[-2]
            leftTotal = totals[-2]
            rightLength = lengths[-1]
            rightTotal = totals[-1]

            leftLast = (leftTotal + leftLength - 1) // leftLength
            rightFirst = rightTotal // rightLength
            if leftLast <= rightFirst:
                break

            lengths[-2] = leftLength + rightLength
            totals[-2] = leftTotal + rightTotal
            lengths.pop()
            totals.pop()

        value = value * value % MOD

    position = 0
    finalPotential = 0

    for length, total in zip(lengths, totals):
        base = total // length
        remainder = total - base * length
        allIndexSum = length * (2 * position + length - 1) // 2
        finalPotential += base * allIndexSum

        if remainder:
            extraStart = position + length - remainder
            extraIndexSum = remainder * (2 * extraStart + remainder - 1) // 2
            finalPotential += extraIndexSum

        position += length

    return finalPotential - initialPotential


def runTests():
    assert B(5) == 0
    assert B(6) == 14_263_289
    assert B(100) == 3_284_417_556


def solve():
    return B(10**7)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
