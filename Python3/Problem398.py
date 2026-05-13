import time


ROPE_LENGTH = 10**7
SEGMENTS = 100


def binomialRatio(top, choose, denominatorTop):
    if top < choose:
        return 0.0

    ratio = 1.0

    for offset in range(choose):
        ratio *= (top - offset) / (denominatorTop - offset)

    return ratio


def expectedSecondShortest(ropeLength=ROPE_LENGTH, segments=SEGMENTS):
    choose = segments - 1
    denominatorTop = ropeLength - 1
    expected = 0.0
    maximumLength = (ropeLength - 1) // (segments - 1)

    for length in range(1, maximumLength + 1):
        allLargeTop = ropeLength - segments * (length - 1) - 1
        oneSmallTop = ropeLength - (segments - 1) * (length - 1) - 1
        allLarge = binomialRatio(allLargeTop, choose, denominatorTop)
        oneSmall = segments * (
            binomialRatio(oneSmallTop, choose, denominatorTop)
            - binomialRatio(oneSmallTop - length + 1, choose, denominatorTop)
        )
        expected += allLarge + oneSmall

    return expected


def answer():
    return format(expectedSecondShortest(), ".5f")


def runTests():
    assert expectedSecondShortest(3, 2) == 2
    assert format(expectedSecondShortest(8, 3), ".5f") == "2.28571"


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = answer()
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")
