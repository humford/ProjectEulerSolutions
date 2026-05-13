import time


MOD = 1_000_000_007
NTT_PRIMES = (
    (998_244_353, 3),
    (1_004_535_809, 3),
    (469_762_049, 3),
)


def ceilingPowerOfTwo(value):
    result = 1
    while result < value:
        result <<= 1
    return result


def bitReversalPermutation(size):
    reversal = [0] * size
    j = 0
    for i in range(1, size):
        bit = size >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        reversal[i] = j
    return reversal


def rootsOfUnity(size, modulus, primitiveRoot):
    root = pow(primitiveRoot, (modulus - 1) // size, modulus)
    roots = [1] * size
    for i in range(1, size):
        roots[i] = roots[i - 1] * root % modulus

    inverseRoot = pow(root, modulus - 2, modulus)
    inverseRoots = [1] * size
    for i in range(1, size):
        inverseRoots[i] = inverseRoots[i - 1] * inverseRoot % modulus

    return roots, inverseRoots


def ntt(values, modulus, roots, inverseRoots, reversal, invert):
    size = len(values)
    for i, j in enumerate(reversal):
        if i < j:
            values[i], values[j] = values[j], values[i]

    length = 2
    rootTable = inverseRoots if invert else roots
    while length <= size:
        half = length // 2
        step = size // length
        for start in range(0, size, length):
            rootIndex = 0
            for index in range(start, start + half):
                u = values[index]
                v = values[index + half] * rootTable[rootIndex] % modulus
                values[index] = (u + v) % modulus
                values[index + half] = (u - v) % modulus
                rootIndex += step
        length *= 2

    if invert:
        inverseSize = pow(size, modulus - 2, modulus)
        for i in range(size):
            values[i] = values[i] * inverseSize % modulus


class ConvolutionContext:
    def __init__(self, size):
        self.size = size
        self.reversal = bitReversalPermutation(size)
        self.tables = []
        for modulus, primitiveRoot in NTT_PRIMES:
            roots, inverseRoots = rootsOfUnity(size, modulus, primitiveRoot)
            self.tables.append((modulus, roots, inverseRoots))

        (p1, _), (p2, _), (p3, _) = NTT_PRIMES
        self.crtConstants = (
            p1,
            p2,
            p3,
            pow(p1, p2 - 2, p2),
            p1 % p3,
            (p1 * p2) % p3,
            pow((p1 * p2) % p3, p3 - 2, p3),
            p1 % MOD,
            (p1 * p2) % MOD,
        )

    def convolution(self, left, right):
        needed = len(left) + len(right) - 1
        residues = []
        for modulus, roots, inverseRoots in self.tables:
            a = [0] * self.size
            b = [0] * self.size
            for index, value in enumerate(left):
                a[index] = value % modulus
            for index, value in enumerate(right):
                b[index] = value % modulus

            ntt(a, modulus, roots, inverseRoots, self.reversal, False)
            ntt(b, modulus, roots, inverseRoots, self.reversal, False)
            for index in range(self.size):
                a[index] = a[index] * b[index] % modulus
            ntt(a, modulus, roots, inverseRoots, self.reversal, True)
            residues.append(a[:needed])

        return self.crtReduce(residues, needed)

    def squareConvolution(self, values):
        needed = 2 * len(values) - 1
        residues = []
        for modulus, roots, inverseRoots in self.tables:
            transformed = [0] * self.size
            for index, value in enumerate(values):
                transformed[index] = value % modulus

            ntt(transformed, modulus, roots, inverseRoots, self.reversal, False)
            for index in range(self.size):
                transformed[index] = transformed[index] * transformed[index] % modulus
            ntt(transformed, modulus, roots, inverseRoots, self.reversal, True)
            residues.append(transformed[:needed])

        return self.crtReduce(residues, needed)

    def crtReduce(self, residues, needed):
        (
            p1,
            p2,
            p3,
            inverseP1ModP2,
            p1ModP3,
            p12ModP3,
            inverseP12ModP3,
            p1ModTarget,
            p12ModTarget,
        ) = self.crtConstants

        result = [0] * needed
        for index in range(needed):
            r1 = residues[0][index]
            r2 = residues[1][index]
            r3 = residues[2][index]

            t1 = (r2 - r1) % p2 * inverseP1ModP2 % p2
            x2ModP3 = (r1 + p1ModP3 * t1) % p3
            t2 = (r3 - x2ModP3) % p3 * inverseP12ModP3 % p3
            result[index] = (
                r1 + p1ModTarget * (t1 % MOD) + p12ModTarget * (t2 % MOD)
            ) % MOD

        return result


def power16(value):
    square = value * value % MOD
    fourth = square * square % MOD
    eighth = fourth * fourth % MOD
    return eighth * eighth % MOD


def B(k, n):
    if n % k != 0:
        raise ValueError("this solver requires n divisible by k")

    repeatCount = n // k
    alternatingWeight = pow(2, repeatCount, MOD)

    factorial = [1] * (k + 1)
    for i in range(1, k + 1):
        factorial[i] = factorial[i - 1] * i % MOD

    inverseFactorial = [1] * (k + 1)
    inverseFactorial[k] = pow(factorial[k], MOD - 2, MOD)
    for i in range(k, 0, -1):
        inverseFactorial[i - 1] = inverseFactorial[i] * i % MOD

    factorial16 = [power16(value) for value in factorial]
    inverseFactorial16 = [power16(value) for value in inverseFactorial]

    transformLength = ceilingPowerOfTwo(2 * (k + 1) - 1)
    context = ConvolutionContext(transformLength)

    franelConvolution = context.squareConvolution(inverseFactorial16)
    franel = [factorial16[r] * franelConvolution[r] % MOD for r in range(k + 1)]

    transformedFranel = [franel[r] * inverseFactorial[r] % MOD for r in range(k + 1)]
    transformKernel = [0] * (k + 1)
    power = 1
    for j in range(k + 1):
        transformKernel[j] = power * inverseFactorial[j] % MOD
        power = power * (MOD - 2) % MOD

    transformedCounts = context.convolution(transformedFranel, transformKernel)
    counts = [transformedCounts[length] * factorial[length] % MOD for length in range(k + 1)]

    powersA = [1] * (k + 1)
    for i in range(1, k + 1):
        powersA[i] = powersA[i - 1] * alternatingWeight % MOD

    answer = 0
    factorialK = factorial[k]
    for alternatingCount in range(k + 1):
        choose = (
            factorialK
            * inverseFactorial[alternatingCount]
            % MOD
            * inverseFactorial[k - alternatingCount]
            % MOD
        )
        answer = (
            answer
            + choose * powersA[alternatingCount] % MOD * counts[k - alternatingCount]
        ) % MOD

    return answer


def runTests():
    assert B(1, 1) == 2
    assert B(1, 4) == 16
    assert B(2, 4) == 65_550
    assert B(3, 9) == 87_273_560


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = B(10 ** 5, 10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
