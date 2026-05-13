import time


MOD = 998_244_353
PRIMITIVE_ROOT = 3


def primeSieve(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for n in range(2, int(limit ** 0.5) + 1):
        if sieve[n]:
            start = n * n
            sieve[start: limit + 1: n] = b"\x00" * ((limit - start) // n + 1)

    return [n for n in range(2, limit + 1) if sieve[n]]


def ntt(values, invert):
    n = len(values)
    j = 0

    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            values[i], values[j] = values[j], values[i]

    length = 2
    while length <= n:
        root = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            root = pow(root, MOD - 2, MOD)

        half = length >> 1
        for start in range(0, n, length):
            w = 1
            for offset in range(half):
                u = values[start + offset]
                v = values[start + offset + half] * w % MOD
                values[start + offset] = (u + v) % MOD
                values[start + offset + half] = (u - v) % MOD
                w = w * root % MOD

        length <<= 1

    if invert:
        inverseN = pow(n, MOD - 2, MOD)
        for i in range(n):
            values[i] = values[i] * inverseN % MOD


def polynomialMultiply(a, b):
    if not a or not b:
        return []

    resultLength = len(a) + len(b) - 1
    if min(len(a), len(b)) <= 32:
        result = [0] * resultLength
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    result[i + j] = (result[i + j] + ai * bj) % MOD
        return result

    size = 1
    while size < resultLength:
        size <<= 1

    fa = a + [0] * (size - len(a))
    fb = b + [0] * (size - len(b))
    ntt(fa, False)
    ntt(fb, False)

    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)
    return fa[:resultLength]


def polynomialDerivative(poly):
    return [i * poly[i] % MOD for i in range(1, len(poly))]


def polynomialIntegral(poly, inverses):
    result = [0] * (len(poly) + 1)
    for i, value in enumerate(poly, 1):
        result[i] = value * inverses[i] % MOD
    return result


def polynomialInverse(poly, length):
    result = [pow(poly[0], MOD - 2, MOD)]
    size = 1

    while size < length:
        nextSize = min(2 * size, length)
        product = polynomialMultiply(poly[:nextSize], result)[:nextSize]
        product[0] = (2 - product[0]) % MOD
        for i in range(1, nextSize):
            product[i] = (-product[i]) % MOD
        result = polynomialMultiply(result, product)[:nextSize]
        size = nextSize

    return result[:length]


def polynomialLog(poly, length, inverses):
    derivative = polynomialDerivative(poly)
    inverse = polynomialInverse(poly, length)
    quotient = polynomialMultiply(derivative, inverse)[: max(0, length - 1)]
    return polynomialIntegral(quotient, inverses)[:length]


def polynomialExp(poly, length, inverses):
    result = [1]
    size = 1

    while size < length:
        nextSize = min(2 * size, length)
        padded = result + [0] * (nextSize - len(result))
        logResult = polynomialLog(padded, nextSize, inverses)
        correction = [0] * nextSize

        for i in range(nextSize):
            correction[i] = ((poly[i] if i < len(poly) else 0) - logResult[i]) % MOD
        correction[0] = (correction[0] + 1) % MOD

        result = polynomialMultiply(result, correction)[:nextSize]
        size = nextSize

    return result[:length]


def specialComponent(limit):
    inverseTwo = (MOD + 1) // 2

    v1 = [0] * (limit + 1)
    v1[0] = 1
    power = 2
    while power <= limit:
        for degree in range(power, limit + 1):
            v1[degree] = (v1[degree] + v1[degree - power]) % MOD
        power <<= 1

    vminus = [0] * (limit + 1)
    vminus[0] = 1
    power = 2
    while power <= limit:
        previous = vminus
        current = [0] * (limit + 1)
        for degree in range(limit + 1):
            value = previous[degree]
            if degree >= power:
                value = (value - current[degree - power]) % MOD
            current[degree] = value
        vminus = current
        power <<= 1

    pSeries = [0] * (limit + 1)
    for degree in range(limit + 1):
        term1 = v1[degree] + (v1[degree - 1] if degree > 0 else 0)
        term2 = vminus[degree] - (vminus[degree - 1] if degree > 0 else 0)
        pSeries[degree] = (term1 + term2) * inverseTwo % MOD

    withLinearFactor = [0] * (limit + 1)
    running = 0
    for degree in range(limit + 1):
        running = (running + pSeries[degree]) % MOD
        withLinearFactor[degree] = running

    result = [0] * (limit + 1)
    for degree in range(limit + 1):
        value = withLinearFactor[degree]
        if degree >= 2:
            value = (value + result[degree - 2]) % MOD
        result[degree] = value

    return result


def addComponentMultiplicities(multiplicities, limit):
    phiLimit = 2 * limit
    primes = [prime for prime in primeSieve(phiLimit + 1) if prime % 2]

    def dfs(startIndex, nValue, phiValue):
        if nValue > 1:
            baseDegree = phiValue // 2
            weight = 0
            k = 0

            while True:
                if k <= 1:
                    degree = baseDegree
                else:
                    degree = phiValue * (1 << (k - 2))

                weight += degree
                if weight > limit:
                    break

                multiplicities[weight] += 1
                k += 1

        for index in range(startIndex, len(primes)):
            prime = primes[index]
            if phiValue * (prime - 1) > phiLimit:
                break

            nextN = nValue * prime
            nextPhi = phiValue * (prime - 1)
            dfs(index + 1, nextN, nextPhi)

            nextN *= prime
            nextPhi *= prime
            while nextPhi <= phiLimit:
                dfs(index + 1, nextN, nextPhi)
                nextN *= prime
                nextPhi *= prime

    dfs(0, 1, 1)


def S(limit):
    multiplicities = [0] * (limit + 1)
    addComponentMultiplicities(multiplicities, limit)

    divisorSums = [0] * (limit + 1)
    for degree in range(1, limit + 1):
        count = multiplicities[degree]
        if count:
            increment = degree * (count % MOD) % MOD
            for multiple in range(degree, limit + 1, degree):
                divisorSums[multiple] = (divisorSums[multiple] + increment) % MOD

    inverses = [0] * (limit + 2)
    for n in range(1, limit + 2):
        inverses[n] = pow(n, MOD - 2, MOD)

    logSeries = [0] * (limit + 1)
    for degree in range(1, limit + 1):
        logSeries[degree] = divisorSums[degree] * inverses[degree] % MOD

    regular = polynomialExp(logSeries, limit + 1, inverses)
    special = specialComponent(limit)
    total = polynomialMultiply(regular, special)[: limit + 1]

    return total[limit] % MOD


def runTests():
    values = [S(n) for n in (2, 5, 20)]
    assert values == [6, 58, 122_087]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
