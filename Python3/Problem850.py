from array import array
from bisect import bisect_left
import math
import time


MOD = 977_676_779
MOD2 = 2 * MOD


def twoF(k, n):
    value = n
    core = 1
    prime = 2

    while prime * prime <= value:
        if value % prime == 0:
            exponent = 0
            while value % prime == 0:
                value //= prime
                exponent += 1
            core *= prime ** ((exponent + k - 1) // k)
        prime += 1 if prime == 2 else 2

    if value > 1:
        core *= value

    return n - n // core


def sieveMobius(limit):
    spf = array("I", [0]) * (limit + 1)
    mobius = array("b", [0]) * (limit + 1)
    primes = []
    mobius[1] = 1

    for n in range(2, limit + 1):
        if spf[n] == 0:
            spf[n] = n
            primes.append(n)
            mobius[n] = -1

        for prime in primes:
            if prime > spf[n]:
                break
            multiple = n * prime
            if multiple > limit:
                break
            spf[multiple] = prime
            if n % prime == 0:
                mobius[multiple] = 0
                break
            mobius[multiple] = -mobius[n]

    prefixMobius = array("i", [0]) * (limit + 1)
    prefixSquarefree = array("i", [0]) * (limit + 1)
    sumMobius = 0
    sumSquarefree = 0

    for n in range(1, limit + 1):
        sumMobius += int(mobius[n])
        prefixMobius[n] = sumMobius
        if mobius[n] != 0:
            sumSquarefree += 1
        prefixSquarefree[n] = sumSquarefree

    return primes, mobius, prefixMobius, prefixSquarefree


def computeTwoSMod(N, modulus2=MOD2):
    if N <= 0:
        return 0

    maxExponent = N.bit_length() - 1
    tailFirst = maxExponent + 1
    if tailFirst % 2 == 0:
        tailFirst += 1

    kList = list(range(3, min(N, tailFirst - 2) + 1, 2))
    kCount = len(kList)

    limit = math.isqrt(N)
    primes, _mobius, prefixMobius, prefixSquarefree = sieveMobius(limit)
    squarefreeCache = {}

    def squarefreeCount(x):
        if x <= 0:
            return 0
        if x <= limit:
            return int(prefixSquarefree[x])
        cached = squarefreeCache.get(x)
        if cached is not None:
            return cached

        root = math.isqrt(x)
        total = 0
        i = 1
        while i <= root:
            quotient = x // (i * i)
            j = math.isqrt(x // quotient)
            total += (int(prefixMobius[j]) - int(prefixMobius[i - 1])) * quotient
            i = j + 1

        squarefreeCache[x] = total
        return total

    def squarefreeCoprimeCount(x, radicalPrimes):
        if x <= 0:
            return 0
        if not radicalPrimes:
            return squarefreeCount(x)

        total = 0

        def dfs(index, product, sign):
            nonlocal total
            if index == len(radicalPrimes):
                total += sign * squarefreeCount(x // product)
                return

            prime = radicalPrimes[index]
            power = 1
            currentSign = sign
            while product * power <= x:
                dfs(index + 1, product * power, currentSign)
                power *= prime
                currentSign = -currentSign

        dfs(0, 1, 1)
        return total

    exponentTable = []
    if kCount:
        exponentTable = [[0] * kCount for _ in range(maxExponent + 1)]
        for exponent in range(2, maxExponent + 1):
            for index, k in enumerate(kList):
                exponentTable[exponent][index] = exponent - ((exponent + k - 1) // k)

    firstKAtLeast = [0] * (maxExponent + 2)
    for exponent in range(maxExponent + 2):
        firstKAtLeast[exponent] = bisect_left(kList, exponent) if kCount else 0

    smallH = [0] * kCount
    diff = [0] * (kCount + 1)
    tailH = 0

    squarefreeTotal = squarefreeCount(N)
    squarefreeMod = squarefreeTotal % modulus2
    tailH = (tailH + squarefreeMod) % modulus2
    if kCount:
        diff[0] += squarefreeMod
        diff[kCount] -= squarefreeMod

    factorPrimes = []
    factorExponents = []

    def processPowerful(powerfulValue, constantMod, maxLocalExponent):
        nonlocal tailH
        count = squarefreeCoprimeCount(N // powerfulValue, factorPrimes)
        countMod = count % modulus2
        amount = constantMod * countMod % modulus2

        tailH = (tailH + amount) % modulus2
        if not kCount:
            return

        suffix = firstKAtLeast[maxLocalExponent] if maxLocalExponent < len(firstKAtLeast) else kCount
        diff[suffix] += amount
        diff[kCount] -= amount

        for position in range(suffix):
            hValue = 1
            for i, prime in enumerate(factorPrimes):
                hValue = hValue * pow(prime, exponentTable[factorExponents[i]][position], modulus2) % modulus2
            smallH[position] = (smallH[position] + hValue * countMod) % modulus2

    def dfs(startIndex, currentValue, constantMod, maxLocalExponent):
        for i in range(startIndex, len(primes)):
            prime = primes[i]
            if currentValue * prime * prime > N:
                break

            value = currentValue * prime * prime
            exponent = 2
            constantPower = prime % modulus2

            while value <= N:
                factorPrimes.append(prime)
                factorExponents.append(exponent)

                nextConstant = constantMod * constantPower % modulus2
                nextMaxExponent = max(maxLocalExponent, exponent)
                processPowerful(value, nextConstant, nextMaxExponent)
                dfs(i + 1, value, nextConstant, nextMaxExponent)

                factorPrimes.pop()
                factorExponents.pop()

                exponent += 1
                value *= prime
                constantPower = constantPower * prime % modulus2

    dfs(0, 1, 1, 0)

    if kCount:
        running = 0
        for position in range(kCount):
            running = (running + diff[position]) % modulus2
            smallH[position] = (smallH[position] + running) % modulus2

    h1 = N % modulus2
    oddCount = (N + 1) // 2
    smallCount = 1 + kCount
    tailCount = oddCount - smallCount
    totalH = (h1 + sum(smallH) + (tailCount % modulus2) * tailH) % modulus2
    sumN = (N * (N + 1) // 2) % modulus2

    return ((oddCount % modulus2) * sumN - totalH) % modulus2


def solve(N):
    return (computeTwoSMod(N, MOD2) // 2) % MOD


def runTests():
    assert twoF(5, 10) == 9
    assert twoF(7, 1234) == 1233
    assert computeTwoSMod(10, MOD2) == 201
    assert computeTwoSMod(10**3, MOD2) == 247_375_608


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve(33_557_799_775_533)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
