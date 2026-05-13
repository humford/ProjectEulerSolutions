import time


MOD = 1_000_000_007
INV2 = (MOD + 1) // 2


def precomputeFactorials(limit):
    factorials = [1] * (limit + 1)
    for n in range(1, limit + 1):
        factorials[n] = factorials[n - 1] * n % MOD

    inverses = [0] * (limit + 1)
    inverses[1] = 1
    for n in range(2, limit + 1):
        inverses[n] = MOD - (MOD // n) * inverses[MOD % n] % MOD

    inverseFactorials = [1] * (limit + 1)
    inverseFactorials[limit] = pow(factorials[limit], MOD - 2, MOD)
    for n in range(limit, 0, -1):
        inverseFactorials[n - 1] = inverseFactorials[n] * n % MOD

    return factorials, inverses, inverseFactorials


def powersOfTwo(limit):
    result = [1] * (limit + 1)
    for n in range(1, limit + 1):
        result[n] = 2 * result[n - 1] % MOD
    return result


class HanoiCoefficientCounter:
    def __init__(self, limit):
        self.factorials, self.inverses, self.inverseFactorials = precomputeFactorials(limit)
        self.pow2 = powersOfTwo(limit)
        self.cache = {}

    def denominatorCoefficient(self, a, b, c):
        key = (a, b, c)
        if key in self.cache:
            return self.cache[key]

        if a < 0 or b < 0 or c < 0:
            self.cache[key] = 0
            return 0
        if (a ^ b) & 1 or (a ^ c) & 1:
            self.cache[key] = 0
            return 0

        minExponent = min(a, b, c)
        sharedTermCount = a & 1
        if sharedTermCount > minExponent:
            self.cache[key] = 0
            return 0

        xTerms = (a - sharedTermCount) // 2
        yTerms = (b - sharedTermCount) // 2
        zTerms = (c - sharedTermCount) // 2
        seriesPower = (a + b + c - sharedTermCount) // 2

        term = self.pow2[sharedTermCount]
        term = term * self.factorials[seriesPower] % MOD
        term = term * self.inverseFactorials[sharedTermCount] % MOD
        term = term * self.inverseFactorials[xTerms] % MOD
        term = term * self.inverseFactorials[yTerms] % MOD
        term = term * self.inverseFactorials[zTerms] % MOD

        total = 0
        while True:
            total = (total + term) % MOD

            nextShared = sharedTermCount + 2
            if nextShared > minExponent:
                break

            ratio = 4 * xTerms % MOD
            ratio = ratio * yTerms % MOD
            ratio = ratio * zTerms % MOD
            ratio = ratio * self.inverses[seriesPower] % MOD
            ratio = ratio * self.inverses[sharedTermCount + 1] % MOD
            ratio = ratio * self.inverses[sharedTermCount + 2] % MOD

            term = term * ratio % MOD
            sharedTermCount = nextShared
            xTerms -= 1
            yTerms -= 1
            zTerms -= 1
            seriesPower -= 1

        self.cache[key] = total
        return total

    def countPositions(self, a, b, c):
        total = self.denominatorCoefficient(a, b, c)
        total += self.denominatorCoefficient(a - 1, b, c)
        total += self.denominatorCoefficient(a, b, c - 1)
        total += self.denominatorCoefficient(a - 1, b - 1, c)
        total += self.denominatorCoefficient(a, b - 1, c - 1)
        total -= self.denominatorCoefficient(a, b - 2, c)
        return total % MOD


def xorZeroTriples(n):
    if n & 1:
        return []

    triples = [(0, 0, 0)]
    bit = 1
    value = n >> 1
    while value:
        if value & 1:
            nextTriples = []
            for a, b, c in triples:
                nextTriples.append((a + bit, b + bit, c))
                nextTriples.append((a + bit, b, c + bit))
                nextTriples.append((a, b + bit, c + bit))
            triples = nextTriples
        bit <<= 1
        value >>= 1

    return triples


def losingPositionCount(n, counter):
    total = 0
    for a, b, c in xorZeroTriples(n):
        total = (total + counter.countPositions(a, b, c)) % MOD
    return total


def f(n):
    if n & 1:
        return 0

    counter = HanoiCoefficientCounter(n + 5)
    count = losingPositionCount(n, counter)
    return count * (pow(2, n, MOD) - 1) * INV2 % MOD


def runTests():
    assert f(4) == 30
    assert f(10) == 67_518


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f(100_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
