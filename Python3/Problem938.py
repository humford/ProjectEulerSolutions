import math
import time


TARGET_R = 24_690
TARGET_B = 12_345


def probabilityClosedForm(redCards, blackCards):
    if blackCards == 0:
        return 0.0
    if redCards == 0:
        return 1.0
    if redCards % 2 == 1:
        return 0.0

    redPairs = redCards // 2
    logComplement = (
        math.lgamma(redPairs + blackCards)
        - math.lgamma(redPairs)
        + math.lgamma(redPairs + 0.5)
        - math.lgamma(redPairs + blackCards + 0.5)
    )
    return 1.0 - math.exp(logComplement)


def probabilityByRecurrence(redCards, blackCards):
    probabilities = [[0.0] * (blackCards + 1) for _ in range(redCards + 1)]

    for black in range(1, blackCards + 1):
        probabilities[0][black] = 1.0

    for red in range(2, redCards + 1):
        for black in range(1, blackCards + 1):
            probabilities[red][black] = (
                (red - 1) * probabilities[red - 2][black]
                + 2 * black * probabilities[red][black - 1]
            ) / (red - 1 + 2 * black)

    return probabilities[redCards][blackCards]


def P(redCards, blackCards):
    return probabilityClosedForm(redCards, blackCards)


def solve():
    return f"{P(TARGET_R, TARGET_B):.10f}"


def runTests():
    assert f"{P(2, 2):.10f}" == "0.4666666667"
    assert f"{P(10, 9):.10f}" == "0.4118903397"
    assert f"{P(34, 25):.10f}" == "0.3665688069"

    for redCards in range(0, 12, 2):
        for blackCards in range(0, 12):
            assert abs(
                probabilityClosedForm(redCards, blackCards)
                - probabilityByRecurrence(redCards, blackCards)
            ) < 1e-12


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
