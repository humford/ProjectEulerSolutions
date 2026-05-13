import time
from math import comb


def v2(n):
    if n == 0:
        return 10 ** 18
    return (n & -n).bit_length() - 1


def inverseModPower2Odd(a, precision, mask):
    inverse = 1
    for _ in range(precision.bit_length() + 1):
        inverse = inverse * (2 - a * inverse) & mask
    return inverse


def u(n, initialPrecision=256, maxTerms=220):
    for precision in (initialPrecision, 2 * initialPrecision, 4 * initialPrecision, 8 * initialPrecision):
        modulus = 1 << precision
        mask = modulus - 1
        inverseCache = {}

        def inverseOdd(a):
            a &= mask
            cached = inverseCache.get(a)
            if cached is None:
                cached = inverseModPower2Odd(a, precision, mask)
                inverseCache[a] = cached
            return cached

        k = n + 1
        exponent = k + k.bit_count()
        oddPart = 1
        minExponent = None
        scaledSum = 0

        for terms in range(1, maxTerms + 1):
            if minExponent is None:
                minExponent = exponent
                scaledSum = oddPart & mask
            elif exponent < minExponent:
                shift = minExponent - exponent
                scaledSum = (scaledSum << shift) & mask if shift < precision else 0
                minExponent = exponent
                scaledSum = (scaledSum + oddPart) & mask
            else:
                shift = exponent - minExponent
                if shift < precision:
                    scaledSum = (scaledSum + ((oddPart << shift) & mask)) & mask

            if scaledSum == 0:
                break

            partialValuation = minExponent + v2(scaledSum)
            if partialValuation < n + terms + 1:
                return partialValuation

            denominator = k + 1
            denominatorTwos = v2(denominator)
            denominatorOdd = denominator >> denominatorTwos

            oddMultiplier = (-(2 * k + 1) * inverseOdd(denominatorOdd)) & mask
            oddPart = oddPart * oddMultiplier & mask
            exponent += 2 - denominatorTwos
            k = denominator

            assert exponent == k + k.bit_count()

    raise RuntimeError("insufficient 2-adic precision")


def U(N):
    return sum(u(n * n * n) for n in range(1, N + 1))


def naiveS(n):
    total = 0
    for k in range(1, n + 1):
        total += (-2) ** k * comb(2 * k, k)
    return total


def runTests():
    assert naiveS(4) == 980
    assert 3 * naiveS(4) + 4 == 2_944
    assert u(4) == 7
    assert u(20) == 24
    assert U(5) == 241


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = U(10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
