from bisect import bisect_right
import time


def buildSmallestPrimeFactor(limit):
    spf = [0] * (limit + 1)
    primes = []

    for n in range(2, limit + 1):
        if spf[n] == 0:
            spf[n] = n
            primes.append(n)

        for prime in primes:
            multiple = n * prime
            if multiple > limit:
                break
            spf[multiple] = prime
            if prime == spf[n]:
                break

    if limit >= 1:
        spf[1] = 1
    return spf


def oddPartAndPowerOfTwo(n):
    powerOfTwo = n & -n
    return n // powerOfTwo, powerOfTwo


def divisorData(n, spf):
    if n == 1:
        return [1], [0, 1], 1

    factors = []
    value = n
    while value > 1:
        prime = spf[value]
        exponent = 0
        while value % prime == 0:
            value //= prime
            exponent += 1
        factors.append((prime, exponent))

    divisors = [1]
    for prime, exponent in factors:
        existing = list(divisors)
        power = 1
        for _ in range(exponent):
            power *= prime
            for divisor in existing:
                divisors.append(divisor * power)

    divisors.sort()
    prefix = [0]
    total = 0
    for divisor in divisors:
        total += divisor
        prefix.append(total)

    return divisors, prefix, total


def countAndSumProductsGreaterThan(smallDivisors, largeDivisors, largePrefix, largeTotal, bound):
    count = 0
    total = 0

    for divisor in smallDivisors:
        index = bisect_right(largeDivisors, bound // divisor)
        count += len(largeDivisors) - index
        total += divisor * (largeTotal - largePrefix[index])

    return count, total


def TFromDivisorData(n, powerOfTwo, dataA, dataB):
    divA, prefixA, sumA = dataA
    divB, prefixB, sumB = dataB

    if len(divA) <= len(divB):
        small, large, largePrefix, largeTotal = divA, divB, prefixB, sumB
    else:
        small, large, largePrefix, largeTotal = divB, divA, prefixA, sumA

    oddCount, oddSum = countAndSumProductsGreaterThan(
        small,
        large,
        largePrefix,
        largeTotal,
        n,
    )
    evenCount, evenOddPartSum = countAndSumProductsGreaterThan(
        small,
        large,
        largePrefix,
        largeTotal,
        n // powerOfTwo,
    )

    validCount = oddCount + evenCount
    validDivisorSum = oddSum + powerOfTwo * evenOddPartSum
    return validDivisorSum - n * validCount


def factorParts(n):
    if n % 2:
        evenPart = n - 1
        oddNeighbor = n
    else:
        evenPart = n
        oddNeighbor = n - 1

    oddEvenPart, powerOfTwo = oddPartAndPowerOfTwo(evenPart)
    return oddEvenPart, oddNeighbor, powerOfTwo


def T(n, spf):
    oddEvenPart, oddNeighbor, powerOfTwo = factorParts(n)
    dataA = divisorData(oddEvenPart, spf)
    dataB = divisorData(oddNeighbor, spf)
    return TFromDivisorData(n, powerOfTwo, dataA, dataB)


def U(limit):
    spf = buildSmallestPrimeFactor(limit)
    lastA = None
    lastB = None
    dataA = None
    dataB = None
    total = 0

    for n in range(3, limit + 1):
        oddEvenPart, oddNeighbor, powerOfTwo = factorParts(n)

        if oddEvenPart != lastA:
            dataA = divisorData(oddEvenPart, spf)
            lastA = oddEvenPart
        if oddNeighbor != lastB:
            dataB = divisorData(oddNeighbor, spf)
            lastB = oddNeighbor

        total += TFromDivisorData(n, powerOfTwo, dataA, dataB)

    return total


def SSet(n):
    spf = buildSmallestPrimeFactor(max(3, n))
    oddEvenPart, oddNeighbor, powerOfTwo = factorParts(n)
    divA = divisorData(oddEvenPart, spf)[0]
    divB = divisorData(oddNeighbor, spf)[0]
    indices = []

    for a in divA:
        for b in divB:
            oddDivisor = a * b
            if oddDivisor > n:
                indices.append(oddDivisor - n)
            if powerOfTwo * oddDivisor > n:
                indices.append(powerOfTwo * oddDivisor - n)

    return sorted(indices)


def runTests():
    spf = buildSmallestPrimeFactor(100)
    assert SSet(10) == [5, 8, 20, 35, 80]
    assert T(10, spf) == 148
    assert T(100, spf) == 21828
    assert U(100) == 612572


def solve():
    return U(1_234_567)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
