from math import factorial
import time


TARGET_N = 18
MODULUS = 1123455689


def S(maxDigits, modulus=None):
    factorials = [factorial(n) for n in range(maxDigits + 1)]
    powersOfTen = [1] * (maxDigits + 1)
    repunits = [0] * (maxDigits + 1)

    for length in range(1, maxDigits + 1):
        powersOfTen[length] = 10 * powersOfTen[length - 1]
        repunits[length] = 10 * repunits[length - 1] + 1

    total = 0

    def addContribution(contribution):
        nonlocal total
        if modulus is None:
            total += contribution
        else:
            total = (total + contribution) % modulus

    def search(digit, usedDigits, denominator, sortedValue):
        if digit == 10:
            if usedDigits == 0:
                return

            for length in range(usedDigits, maxDigits + 1):
                zeroCount = length - usedDigits
                ways = (
                    usedDigits * factorials[length - 1]
                    // (factorials[zeroCount] * denominator)
                )
                addContribution(ways * sortedValue)
            return

        for count in range(maxDigits - usedDigits + 1):
            nextValue = sortedValue * powersOfTen[count] + digit * repunits[count]
            search(
                digit + 1,
                usedDigits + count,
                denominator * factorials[count],
                nextValue,
            )

    search(1, 0, 1, 0)
    return total


def solve():
    return S(TARGET_N, MODULUS)


def runTests():
    assert S(1) == 45
    assert S(5) == 1543545675
    assert solve() == 827850196


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
