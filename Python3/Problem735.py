import time
from array import array
from math import isqrt


SQUAREFREE_PREFIX_LIMIT = 20_000_000


def integerCubeRoot(number):
    root = int(round(number ** (1.0 / 3.0)))
    while (root + 1) ** 3 <= number:
        root += 1
    while root ** 3 > number:
        root -= 1
    return root


def mobiusSieve(limit):
    mobius = array("i", [0]) * (limit + 1)
    mobius[1] = 1
    primes = []
    isComposite = bytearray(limit + 1)

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            mobius[number] = -1
        for prime in primes:
            multiple = number * prime
            if multiple > limit:
                break
            isComposite[multiple] = 1
            if number % prime == 0:
                mobius[multiple] = 0
                break
            mobius[multiple] = -mobius[number]

    return mobius


def oddSquarefreePrefix(limit):
    isSquarefree = bytearray(b"\x01") * (limit + 1)
    isSquarefree[0] = 0
    isSquarefree[0::2] = b"\x00" * ((limit // 2) + 1)

    root = isqrt(limit)
    isPrime = bytearray(b"\x01") * (root + 1)
    if root >= 0:
        isPrime[0] = 0
    if root >= 1:
        isPrime[1] = 0

    for number in range(2, isqrt(root) + 1):
        if isPrime[number]:
            start = number * number
            isPrime[start : root + 1 : number] = b"\x00" * (((root - start) // number) + 1)

    for prime in range(3, root + 1, 2):
        if isPrime[prime]:
            square = prime * prime
            isSquarefree[square : limit + 1 : square] = b"\x00" * (((limit - square) // square) + 1)

    prefix = array("I", [0]) * (limit + 1)
    count = 0
    for number in range(1, limit + 1):
        count += isSquarefree[number]
        prefix[number] = count

    return prefix


def divisorCountUpToN(number):
    target = 2 * number * number
    return sum(1 for divisor in range(1, number + 1) if target % divisor == 0)


def bruteForceDivisorCountPrefix(limit):
    return sum(divisorCountUpToN(number) for number in range(1, limit + 1))


def summatoryDivisorCount(limit, prefixLimit=SQUAREFREE_PREFIX_LIMIT):
    if limit < 1:
        return 0

    # Every divisor d of 2*n^2 has one of two forms:
    #   d = q^2*u, or d = q^2*u/2 when q is even,
    # with u odd and squarefree. After summing over n first, the q terms
    # cancel, leaving two factor-pair sums weighted by odd-squarefree counts.
    smallLimit = min(prefixLimit, max(10_000, integerCubeRoot(limit * limit)))
    squarefreePrefix = oddSquarefreePrefix(smallLimit)

    doubleLimit = 2 * limit
    mobiusLimit = isqrt(doubleLimit)
    mobius = mobiusSieve(mobiusLimit)

    oddMobiusPrefix = array("i", [0]) * (mobiusLimit + 1)
    totalMobius = 0
    for number in range(1, mobiusLimit + 1):
        if number & 1:
            totalMobius += mobius[number]
        oddMobiusPrefix[number] = totalMobius

    oddMobiusSquareSumCache = {}

    def oddMobiusSquareSum(value):
        cached = oddMobiusSquareSumCache.get(value)
        if cached is not None:
            return cached

        root = isqrt(value)
        directLimit = min(root, integerCubeRoot(value))

        total = 0
        for number in range(1, directLimit + 1, 2):
            total += mobius[number] * (value // (number * number))

        if directLimit < root:
            largestQuotient = value // ((directLimit + 1) * (directLimit + 1))
            for quotient in range(1, largestQuotient + 1):
                high = isqrt(value // quotient)
                low = isqrt(value // (quotient + 1)) + 1
                if low <= directLimit:
                    low = directLimit + 1
                if low <= high:
                    total += quotient * (oddMobiusPrefix[high] - oddMobiusPrefix[low - 1])

        oddMobiusSquareSumCache[value] = total
        return total

    oddSquarefreeCountCache = {}

    def oddSquarefreeCount(value):
        if value <= smallLimit:
            return int(squarefreePrefix[value])

        cached = oddSquarefreeCountCache.get(value)
        if cached is not None:
            return cached

        count = oddMobiusSquareSum(value) - oddMobiusSquareSum(value // 2)
        oddSquarefreeCountCache[value] = count
        return count

    productLimit = limit // smallLimit
    doubleProductLimit = doubleLimit // smallLimit

    divisorCounts = array("I", [0]) * (productLimit + 1)
    for divisor in range(1, productLimit + 1):
        for multiple in range(divisor, productLimit + 1, divisor):
            divisorCounts[multiple] += 1

    firstSmallSum = 0
    for product in range(1, productLimit + 1):
        root = isqrt(product)
        squareCorrection = 1 if root * root == product else 0
        unorderedPairs = (int(divisorCounts[product]) - squareCorrection) // 2
        if unorderedPairs:
            firstSmallSum += unorderedPairs * oddSquarefreeCount(limit // product)

    firstLargeSum = 0
    maxLeftFactor = isqrt(limit)
    for leftFactor in range(1, maxLeftFactor + 1):
        rightFactor = max(leftFactor + 1, productLimit // leftFactor + 1)
        maxRightFactor = limit // leftFactor
        while rightFactor <= maxRightFactor:
            quotient = limit // (leftFactor * rightFactor)
            lastRightFactor = min(maxRightFactor, limit // (leftFactor * quotient))
            firstLargeSum += (lastRightFactor - rightFactor + 1) * int(squarefreePrefix[quotient])
            rightFactor = lastRightFactor + 1

    evenPairCounts = array("I", [0]) * (doubleProductLimit + 1)
    for leftFactor in range(2, doubleProductLimit + 1, 2):
        maxRightFactor = doubleProductLimit // leftFactor
        if maxRightFactor > leftFactor:
            for rightFactor in range(leftFactor + 1, maxRightFactor + 1):
                evenPairCounts[leftFactor * rightFactor] += 1

    secondSmallSum = 0
    for product in range(1, doubleProductLimit + 1):
        count = int(evenPairCounts[product])
        if count:
            secondSmallSum += count * oddSquarefreeCount(doubleLimit // product)

    secondLargeSum = 0
    maxEvenLeftFactor = isqrt(doubleLimit)
    for leftFactor in range(2, maxEvenLeftFactor + 1, 2):
        rightFactor = max(leftFactor + 1, doubleProductLimit // leftFactor + 1)
        maxRightFactor = doubleLimit // leftFactor
        while rightFactor <= maxRightFactor:
            quotient = doubleLimit // (leftFactor * rightFactor)
            lastRightFactor = min(maxRightFactor, doubleLimit // (leftFactor * quotient))
            secondLargeSum += (lastRightFactor - rightFactor + 1) * int(squarefreePrefix[quotient])
            rightFactor = lastRightFactor + 1

    return limit + firstSmallSum + firstLargeSum + secondSmallSum + secondLargeSum


def runTests():
    assert divisorCountUpToN(15) == 8
    assert bruteForceDivisorCountPrefix(15) == 63
    assert summatoryDivisorCount(15) == 63
    assert bruteForceDivisorCountPrefix(1_000) == 15_066
    assert summatoryDivisorCount(1_000) == 15_066


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = summatoryDivisorCount(10**12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
