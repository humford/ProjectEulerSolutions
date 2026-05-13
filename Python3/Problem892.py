from array import array
import time


MODULUS = 1_234_567_891
TARGET_N = 10_000_000


def centralBinomialMod(r, modulus=MODULUS):
    value = 1

    for index in range(1, r + 1):
        value = value * (r + index) % modulus
        value = value * pow(index, modulus - 2, modulus) % modulus

    return value


def D(n, modulus=MODULUS):
    if n <= 1:
        return 0

    if n % 2 == 0:
        r = n // 2
        binomial = centralBinomialMod(r, modulus)
        return binomial * binomial * ((modulus + 1) // 2) % modulus

    r = n // 2
    binomial = centralBinomialMod(r, modulus)
    return (
        binomial
        * binomial
        * (2 * r)
        * pow(r + 1, modulus - 2, modulus)
    ) % modulus


def inverseTable(limit, modulus):
    inverses = array("I", [0]) * (limit + 1)
    inverses[1] = 1

    for value in range(2, limit + 1):
        inverses[value] = (
            modulus
            - (modulus // value) * inverses[modulus % value] % modulus
        ) % modulus

    return inverses


def sumD(limit=TARGET_N, modulus=MODULUS):
    rMax = limit // 2
    inverses = inverseTable(rMax + 1, modulus)
    inverseTwo = (modulus + 1) // 2

    central = 1
    total = 0

    for r in range(rMax + 1):
        centralSquared = central * central % modulus

        if r:
            total += centralSquared * inverseTwo
            total %= modulus

        if r and 2 * r + 1 <= limit:
            total += centralSquared * (2 * r) % modulus * inverses[r + 1]
            total %= modulus

        if r < rMax:
            inverse = inverses[r + 1]
            central = central * (2 * r + 1) % modulus
            central = central * (2 * r + 2) % modulus
            central = central * inverse % modulus
            central = central * inverse % modulus

    return total


def solve():
    return sumD(TARGET_N)


def runTests():
    assert D(3) == 4
    assert D(100) == 1172122931
    assert solve() == 469137427


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
