import time


TARGET_N = 10**17
TARGET_M = 1_000_000


def xorProduct(a, b):
    product = 0

    while b:
        if b & 1:
            product ^= a
        a <<= 1
        b >>= 1

    return product


def xorNorm(a, b):
    return xorProduct(a, a) ^ (xorProduct(a, b) << 1) ^ xorProduct(b, b)


def previousUnitStep(a, b):
    return b ^ (a << 1), a


def nextUnitStep(a, b):
    return b, a ^ (b << 1)


def isCanonicalRepresentative(a, b):
    if a == 0 and b == 0:
        return True

    previousA, previousB = previousUnitStep(a, b)
    return previousA > previousB


def representativeLimit(maximumK):
    degree = maximumK.bit_length() - 1
    return 1 << ((degree + 1) // 2 + 1)


def canonicalRepresentatives(maximumK):
    limit = representativeLimit(maximumK)
    squares = [xorProduct(n, n) for n in range(limit)]

    for a in range(limit):
        squareA = squares[a]
        for b in range(a, limit):
            if not isCanonicalRepresentative(a, b):
                continue

            value = squareA ^ (xorProduct(a, b) << 1) ^ squares[b]
            if value <= maximumK:
                yield a, b


def orbitCount(a, b, limit):
    if a == 0 and b == 0:
        return 1

    count = 0
    while b <= limit:
        count += 1
        a, b = nextUnitStep(a, b)

    return count


def G(limitN, maximumK):
    return sum(
        orbitCount(a, b, limitN)
        for a, b in canonicalRepresentatives(maximumK)
    )


def bruteG(limitN, maximumK):
    count = 0

    for a in range(limitN + 1):
        for b in range(a, limitN + 1):
            if xorNorm(a, b) <= maximumK:
                count += 1

    return count


def solve():
    return G(TARGET_N, TARGET_M)


def runTests():
    assert xorProduct(7, 3) == 9
    assert xorNorm(3, 6) == 5
    assert G(20, 100) == bruteG(20, 100) == 105
    assert G(100, 100) == bruteG(100, 100) == 223
    assert G(1000, 100) == 398
    assert solve() == 23707109


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
