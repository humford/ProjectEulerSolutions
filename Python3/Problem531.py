import math
import time


def totientSieve(limit):
    phi = list(range(limit))
    for number in range(2, limit):
        if phi[number] == number:
            for multiple in range(number, limit, number):
                phi[multiple] -= phi[multiple] // number
    return phi


def chineseRemainder(a, n, b, m):
    gcd = math.gcd(n, m)
    if (b - a) % gcd:
        return 0

    nReduced = n // gcd
    mReduced = m // gcd
    multiplier = ((b - a) // gcd * pow(nReduced, -1, mReduced)) % mReduced
    return (a + n * multiplier) % (n * mReduced)


def chineseLeftoversSum(start, stop):
    phi = totientSieve(stop)
    total = 0

    for n in range(start, stop):
        phiN = phi[n]
        for m in range(n + 1, stop):
            total += chineseRemainder(phiN, n, phi[m], m)

    return total


def runTests():
    assert chineseRemainder(2, 4, 4, 6) == 10
    assert chineseRemainder(3, 4, 4, 6) == 0
    assert chineseLeftoversSum(10, 15) == 680


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = chineseLeftoversSum(1_000_000, 1_005_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
