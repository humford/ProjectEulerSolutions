import time
from array import array


def sieveMobiusPhi(limit):
    mobius = array("b", [0]) * (limit + 1)
    phi = array("I", [0]) * (limit + 1)
    isComposite = bytearray(limit + 1)
    primes = []

    mobius[1] = 1
    phi[1] = 1

    for n in range(2, limit + 1):
        if not isComposite[n]:
            primes.append(n)
            mobius[n] = -1
            phi[n] = n - 1

        for prime in primes:
            value = n * prime
            if value > limit:
                break
            isComposite[value] = 1
            if n % prime == 0:
                mobius[value] = 0
                phi[value] = phi[n] * prime
                break
            mobius[value] = -mobius[n]
            phi[value] = phi[n] * (prime - 1)

    mobiusPrefix = array("q", [0]) * (limit + 1)
    phiPrefix = array("q", [0]) * (limit + 1)
    oddMobiusPrefix = array("q", [0]) * (limit + 1)

    for n in range(1, limit + 1):
        mobiusPrefix[n] = mobiusPrefix[n - 1] + mobius[n]
        phiPrefix[n] = phiPrefix[n - 1] + phi[n]
        oddMobiusPrefix[n] = oddMobiusPrefix[n - 1] + (mobius[n] if n % 2 else 0)

    return mobiusPrefix, phiPrefix, oddMobiusPrefix


def makeSummatoryFunctions(N):
    limit = min(int(N ** (2 / 3)) + 10, N)
    mobiusPrefix, phiPrefix, oddMobiusPrefix = sieveMobiusPhi(limit)
    mobiusCache = {}
    phiCache = {}
    oddMobiusCache = {}

    def summatoryMobius(n):
        if n <= limit:
            return int(mobiusPrefix[n])
        cached = mobiusCache.get(n)
        if cached is not None:
            return cached

        total = 1
        left = 2
        while left <= n:
            quotient = n // left
            right = n // quotient
            total -= (right - left + 1) * summatoryMobius(quotient)
            left = right + 1

        mobiusCache[n] = total
        return total

    def summatoryPhi(n):
        if n <= limit:
            return int(phiPrefix[n])
        cached = phiCache.get(n)
        if cached is not None:
            return cached

        total = n * (n + 1) // 2
        left = 2
        while left <= n:
            quotient = n // left
            right = n // quotient
            total -= (right - left + 1) * summatoryPhi(quotient)
            left = right + 1

        phiCache[n] = total
        return total

    def summatoryOddMobius(n):
        if n <= limit:
            return int(oddMobiusPrefix[n])
        cached = oddMobiusCache.get(n)
        if cached is not None:
            return cached

        total = summatoryMobius(n) + summatoryOddMobius(n // 2)
        oddMobiusCache[n] = total
        return total

    return summatoryPhi, summatoryOddMobius


def losingRegionCount(M):
    t = (M - 1) // 4
    if t <= 0:
        return 0
    return t * ((M + 1) // 2) - t * (t + 1)


def H(N):
    summatoryPhi, summatoryOddMobius = makeSummatoryFunctions(N)

    totalPositions = summatoryPhi(N) - 1
    losingUnordered = 0
    divisor = 1

    while divisor <= N:
        quotient = N // divisor
        nextDivisor = N // quotient
        mobiusRange = summatoryOddMobius(nextDivisor) - summatoryOddMobius(divisor - 1)
        losingUnordered += mobiusRange * losingRegionCount(quotient)
        divisor = nextDivisor + 1

    return totalPositions - 2 * losingUnordered


def runTests():
    assert H(4) == 5
    assert H(100) == 2_043


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = H(10 ** 9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
