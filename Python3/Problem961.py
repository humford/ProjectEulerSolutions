import time


TARGET_POWER = 18


def WPower10(power):
    winningTotal = 0
    losingEvenTotal = 0

    for length in range(1, power + 1):
        count = 9 * 10 ** (length - 1)

        if length % 2:
            winning = count
        else:
            winning = 9 * (1 + losingEvenTotal)
            losingEvenTotal += count - winning

        winningTotal += winning

    return winningTotal


def solve():
    return WPower10(TARGET_POWER)


def runTests():
    assert WPower10(2) == 18
    assert WPower10(4) == 1_656


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
