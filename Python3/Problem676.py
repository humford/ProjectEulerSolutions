import time


MODULUS = 10 ** 16
TARGET = 10 ** 16


def digitSum(number, base):
    total = 0
    while number:
        total += number % base
        number //= base
    return total


def matchingDigitSum(limit, firstPower, secondPower):
    bits = [int(bit) for bit in bin(limit)[2:]]
    bitCount = len(bits)
    tight = {0: (1, 0)}
    loose = {}

    def addState(states, difference, count, total):
        oldCount, oldTotal = states.get(difference, (0, 0))
        states[difference] = (oldCount + count, oldTotal + total)

    for index, bitLimit in enumerate(bits):
        position = bitCount - index - 1
        differenceDelta = (
            (1 << (position % firstPower))
            - (1 << (position % secondPower))
        )
        placeValue = 1 << position

        nextTight = {}
        nextLoose = {}

        for difference, (count, total) in loose.items():
            addState(nextLoose, difference, count, total)
            addState(
                nextLoose,
                difference + differenceDelta,
                count,
                total + placeValue * count,
            )

        for difference, (count, total) in tight.items():
            if bitLimit == 0:
                addState(nextTight, difference, count, total)
            else:
                addState(nextLoose, difference, count, total)
                addState(
                    nextTight,
                    difference + differenceDelta,
                    count,
                    total + placeValue * count,
                )

        tight = nextTight
        loose = nextLoose

    return tight.get(0, (0, 0))[1] + loose.get(0, (0, 0))[1]


def matchingDigitTotal(limit=TARGET):
    total = 0
    for firstPower in range(3, 7):
        for secondPower in range(1, firstPower - 1):
            total += matchingDigitSum(limit, firstPower, secondPower)
    return total % MODULUS


def runTests():
    assert digitSum(9, 2) == 2
    assert digitSum(9, 4) == 3
    assert digitSum(17, 4) == digitSum(17, 2) == 2
    assert matchingDigitSum(10, 3, 1) == 18
    assert matchingDigitSum(100, 3, 1) == 292
    assert matchingDigitSum(10 ** 6, 3, 1) == 19_173_952


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = matchingDigitTotal()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
