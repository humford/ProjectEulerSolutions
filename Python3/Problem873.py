from math import comb
import time


MOD = 1_000_000_007


def transitionWords(p, q, transitions):
    if p == 0 or q == 0:
        return 1 if transitions == 0 else 0

    if transitions == 0:
        return 0

    if transitions % 2:
        runs = (transitions + 1) // 2
        return 2 * comb(p - 1, runs - 1) * comb(q - 1, runs - 1)

    runs = transitions // 2
    total = 0
    if runs <= q and runs + 1 <= p:
        total += comb(p - 1, runs) * comb(q - 1, runs - 1)
    if runs <= p and runs + 1 <= q:
        total += comb(p - 1, runs - 1) * comb(q - 1, runs)
    return total


def WExact(p, q, r):
    letters = p + q
    total = 0

    for transitions in range(0, 2 * min(p, q) + 1):
        words = transitionWords(p, q, transitions)
        remainingCs = r - 2 * transitions
        if words and remainingCs >= 0:
            total += words * comb(remainingCs + letters, letters)

    return total


def initialGapBinomial(p, q, r):
    letters = p + q
    numerator = 1
    denominator = 1

    for i in range(1, letters + 1):
        numerator = numerator * (r + i) % MOD
        denominator = denominator * i % MOD

    return numerator * pow(denominator, MOD - 2, MOD) % MOD


def WMod(p, q, r, modulus=MOD):
    letters = p + q
    limit = 2 * min(p, q)

    inverse = [0] * (min(p, q) + 1)
    if len(inverse) > 1:
        inverse[1] = 1
    for i in range(2, len(inverse)):
        inverse[i] = modulus - (modulus // i) * inverse[modulus % i] % modulus

    gapWays = initialGapBinomial(p, q, r)
    currentTransition = 0

    def advanceGapWays():
        nonlocal gapWays, currentTransition
        remaining = r - 2 * currentTransition
        gapWays = (
            gapWays
            * remaining
            % modulus
            * (remaining - 1)
            % modulus
            * pow(remaining + letters, modulus - 2, modulus)
            % modulus
            * pow(remaining + letters - 1, modulus - 2, modulus)
            % modulus
        )
        currentTransition += 1

    total = 0
    aPrevious = 1
    bPrevious = 1

    for runs in range(1, min(p, q) + 1):
        advanceGapWays()
        oddWords = 2 * aPrevious % modulus * bPrevious % modulus
        total = (total + oddWords * gapWays) % modulus

        aCurrent = aPrevious * (p - runs) % modulus * inverse[runs] % modulus
        bCurrent = bPrevious * (q - runs) % modulus * inverse[runs] % modulus

        advanceGapWays()
        evenWords = (
            aCurrent * bPrevious
            + aPrevious * bCurrent
        ) % modulus
        total = (total + evenWords * gapWays) % modulus

        aPrevious = aCurrent
        bPrevious = bCurrent

    return total


def runTests():
    assert WExact(2, 2, 4) == 32
    assert WMod(2, 2, 4) == 32
    assert WExact(4, 4, 44) == 13_908_607_644
    assert WMod(4, 4, 44) == 13_908_607_644 % MOD


def solve():
    return WMod(10**6, 10**7, 10**8)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
