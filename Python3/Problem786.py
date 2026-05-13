import time


def floorSum(n, modulus, a, b):
    total = 0

    while True:
        if a >= modulus:
            total += (n - 1) * n * (a // modulus) // 2
            a %= modulus
        if b >= modulus:
            total += n * (b // modulus)
            b %= modulus

        yMax = a * n + b
        if yMax < modulus:
            return total

        n, b = divmod(yMax, modulus)
        modulus, a = a, modulus


def integerCubeRoot(n):
    if n <= 0:
        return 0

    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            break
        x = y

    while (x + 1) ** 3 <= n:
        x += 1
    while x ** 3 > n:
        x -= 1
    return x


def mobiusPrefix(limit):
    mobius = [0] * (limit + 1)
    isComposite = bytearray(limit + 1)
    primes = []
    mobius[1] = 1

    for n in range(2, limit + 1):
        if not isComposite[n]:
            primes.append(n)
            mobius[n] = -1

        for prime in primes:
            value = n * prime
            if value > limit:
                break
            isComposite[value] = 1
            if n % prime == 0:
                mobius[value] = 0
                break
            mobius[value] = -mobius[n]

    prefix = [0] * (limit + 1)
    total = 0
    for n in range(1, limit + 1):
        total += mobius[n]
        prefix[n] = total
    return prefix


def makeMertens(limit):
    prefix = mobiusPrefix(limit)
    mertensCache = {}
    nonThreeCache = {0: 0}

    def mertens(n):
        if n <= limit:
            return prefix[n]
        cached = mertensCache.get(n)
        if cached is not None:
            return cached

        total = 1
        left = 2
        while left <= n:
            quotient = n // left
            right = n // quotient
            total -= (right - left + 1) * mertens(quotient)
            left = right + 1

        mertensCache[n] = total
        return total

    def nonThreeMobiusPrefix(n):
        if n <= 0:
            return 0
        cached = nonThreeCache.get(n)
        if cached is not None:
            return cached

        total = mertens(n) + nonThreeMobiusPrefix(n // 3)
        nonThreeCache[n] = total
        return total

    return nonThreeMobiusPrefix


def countNonprimitivePoints(M):
    if M < 28:
        return 0

    maxY = (M - 18) // 10
    b = M - 10 * maxY
    total = floorSum(maxY, 18, 10, b)

    maxYMultiple3 = maxY // 3
    b3 = M - 30 * maxYMultiple3
    totalMultiple3 = floorSum(maxYMultiple3, 18, 30, b3)

    return total - totalMultiple3


def countPrimitivePoints(M):
    maxDivisor = M // 28
    if maxDivisor <= 0:
        return 0

    sieveLimit = integerCubeRoot(maxDivisor * maxDivisor) + 64
    nonThreeMobiusPrefix = makeMertens(sieveLimit)

    total = 0
    left = 1
    while left <= maxDivisor:
        quotient = M // left
        right = min(M // quotient, maxDivisor)

        coefficient = nonThreeMobiusPrefix(right) - nonThreeMobiusPrefix(left - 1)
        if coefficient:
            total += coefficient * countNonprimitivePoints(quotient)

        left = right + 1

    return total


def B(N):
    return 2 + 4 * countPrimitivePoints(3 * N + 6)


def runTests():
    assert B(10) == 6
    assert B(100) == 478
    assert B(1000) == 45_790


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = B(10 ** 9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
