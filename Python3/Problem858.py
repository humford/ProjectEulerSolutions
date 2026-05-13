from math import gcd, isqrt
import time


MOD = 1_000_000_007


def primeSieve(limit):
    if limit < 2:
        return []

    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if isPrime[p]:
            isPrime[p * p:limit + 1:p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [n for n in range(2, limit + 1) if isPrime[n]]


def bruteG(limit):
    counts = {1: 1}
    for value in range(1, limit + 1):
        nextCounts = dict(counts)
        for lcmValue, count in counts.items():
            newLcm = lcmValue * value // gcd(lcmValue, value)
            nextCounts[newLcm] = nextCounts.get(newLcm, 0) + count
        counts = nextCounts
    return sum(lcmValue * count for lcmValue, count in counts.items())


def G(limit):
    primes = primeSieve(limit)
    root = isqrt(limit)
    exponents = {}
    inversePrimePower = {}
    lcmMod = 1

    for prime in primes:
        exponent = 0
        power = prime
        while power <= limit:
            exponent += 1
            power *= prime
        exponents[prime] = exponent
        primePowerMod = pow(prime, exponent, MOD)
        inversePrimePower[prime] = pow(primePowerMod, MOD - 2, MOD)
        lcmMod = lcmMod * primePowerMod % MOD

    smallPrimes = [prime for prime in primes if prime <= root]
    largePrimes = [prime for prime in primes if prime > root]
    maxMultiplier = limit // (root + 1)

    powersOfTwo = [1] * (limit + 1)
    for i in range(1, limit + 1):
        powersOfTwo[i] = powersOfTwo[i - 1] * 2 % MOD

    inverseTwo = (MOD + 1) // 2
    inversePowersOfTwo = [1] * (maxMultiplier + 1)
    for i in range(1, maxMultiplier + 1):
        inversePowersOfTwo[i] = inversePowersOfTwo[i - 1] * inverseTwo % MOD

    prefixMasks = [(1 << i) - 1 for i in range(maxMultiplier + 1)]
    options = {}

    for prime in smallPrimes:
        primeOptions = [(0, 0, 1)]
        for exponent in range(1, exponents[prime] + 1):
            primePower = prime**exponent
            maskN = 0
            for multiple in range(primePower, limit + 1, primePower):
                maskN |= 1 << (multiple - 1)

            maskMultiplier = 0
            if primePower <= maxMultiplier:
                for multiple in range(primePower, maxMultiplier + 1, primePower):
                    maskMultiplier |= 1 << (multiple - 1)

            phi = pow(prime, exponent - 1, MOD) * (prime - 1) % MOD
            weight = MOD - phi * inversePrimePower[prime] % MOD
            primeOptions.append((maskN, maskMultiplier, weight))

        options[prime] = primeOptions

    largeWeights = {}
    for prime in largePrimes:
        largeWeights[prime] = (prime - 1) * pow(prime, MOD - 2, MOD) % MOD

    largeCache = {}

    def largeProduct(maskMultiplier):
        cached = largeCache.get(maskMultiplier)
        if cached is not None:
            return cached

        product = 1
        for prime in largePrimes:
            totalMultipliers = limit // prime
            covered = (maskMultiplier & prefixMasks[totalMultipliers]).bit_count()
            newCount = totalMultipliers - covered
            product = product * (1 - largeWeights[prime] * inversePowersOfTwo[newCount] % MOD) % MOD

        largeCache[maskMultiplier] = product
        return product

    total = 0

    def dfs(index, maskN, maskMultiplier, coefficient):
        nonlocal total
        if index == len(smallPrimes):
            uncovered = limit - maskN.bit_count()
            total = (
                total
                + coefficient * powersOfTwo[uncovered] % MOD * largeProduct(maskMultiplier)
            ) % MOD
            return

        prime = smallPrimes[index]
        for addN, addMultiplier, weight in options[prime]:
            dfs(
                index + 1,
                maskN | addN,
                maskMultiplier | addMultiplier,
                coefficient * weight % MOD,
            )

    dfs(0, 0, 0, 1)
    return lcmMod * total % MOD


def runTests():
    assert bruteG(5) == 528
    assert bruteG(20) == 8_463_108_648_960


def solve():
    return G(800)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
