import time


MOD = 999_676_999
LIMIT = 50_000
REV_CACHE = {}


def smallestPrimeFactors(limit):
    spf = list(range(limit + 1))
    spf[0] = 0
    if limit >= 1:
        spf[1] = 1

    for n in range(2, int(limit**0.5) + 1):
        if spf[n] == n:
            for multiple in range(n * n, limit + 1, n):
                if spf[multiple] == multiple:
                    spf[multiple] = n

    return spf


def buildD(limit):
    spf = smallestPrimeFactors(limit)
    derivative = [0] * (limit + 1)

    for n in range(2, limit + 1):
        prime = spf[n]
        rest = n // prime
        derivative[n] = rest + prime * derivative[rest]

    derivative[1] = 1
    return derivative


def modularInverses(limit, modulus):
    inverses = [0] * (limit + 1)
    inverses[1] = 1

    for n in range(2, limit + 1):
        inverses[n] = (modulus - (modulus // n) * inverses[modulus % n] % modulus) % modulus

    return inverses


def nextPowerOfTwo(n):
    return 1 << (n - 1).bit_length()


def bitReversal(size):
    cached = REV_CACHE.get(size)
    if cached is not None:
        return cached

    bits = size.bit_length() - 1
    reversedIndices = [0] * size
    for i in range(1, size):
        reversedIndices[i] = (reversedIndices[i >> 1] >> 1) | ((i & 1) << (bits - 1))

    REV_CACHE[size] = reversedIndices
    return reversedIndices


def ntt(values, invert, modulus, primitiveRoot):
    size = len(values)
    reversedIndices = bitReversal(size)

    for i, j in enumerate(reversedIndices):
        if i < j:
            values[i], values[j] = values[j], values[i]

    length = 2
    while length <= size:
        root = pow(primitiveRoot, (modulus - 1) // length, modulus)
        if invert:
            root = pow(root, modulus - 2, modulus)

        half = length // 2
        for start in range(0, size, length):
            factor = 1
            for i in range(start, start + half):
                u = values[i]
                v = values[i + half] * factor % modulus
                values[i] = (u + v) % modulus
                values[i + half] = (u - v) % modulus
                factor = factor * root % modulus

        length *= 2

    if invert:
        inverseSize = pow(size, modulus - 2, modulus)
        for i in range(size):
            values[i] = values[i] * inverseSize % modulus


class NTTConvolver:
    PRIMES = (
        (998_244_353, 3),
        (1_004_535_809, 3),
        (469_762_049, 3),
    )

    def __init__(self, fixedValues, outputModulus):
        self.fixedValues = fixedValues
        self.outputModulus = outputModulus
        self.cache = {}
        self.p1 = self.PRIMES[0][0]
        self.p2 = self.PRIMES[1][0]
        self.p3 = self.PRIMES[2][0]
        self.inverseP1ModP2 = pow(self.p1, self.p2 - 2, self.p2)
        self.inverseP12ModP3 = pow((self.p1 * self.p2) % self.p3, self.p3 - 2, self.p3)
        self.p1ModOutput = self.p1 % outputModulus
        self.p12ModOutput = (self.p1 * self.p2) % outputModulus

    def cachedTransform(self, length):
        cached = self.cache.get(length)
        if cached is not None:
            return cached

        fftSize = 2 * length
        transforms = []
        for modulus, root in self.PRIMES:
            values = [0] * fftSize
            for i in range(length):
                values[i] = self.fixedValues[i] % modulus
            ntt(values, False, modulus, root)
            transforms.append(values)

        cached = tuple(transforms)
        self.cache[length] = cached
        return cached

    def convolveFirstLength(self, segment, length):
        if not segment:
            return [0] * length

        fftSize = 2 * length
        fixedTransforms = self.cachedTransform(length)
        residues = []

        for (modulus, root), fixedTransform in zip(self.PRIMES, fixedTransforms):
            values = [0] * fftSize
            for i, value in enumerate(segment):
                values[i] = value % modulus
            ntt(values, False, modulus, root)
            for i in range(fftSize):
                values[i] = values[i] * fixedTransform[i] % modulus
            ntt(values, True, modulus, root)
            residues.append(values[:length])

        first, second, third = residues
        output = [0] * length

        for i in range(length):
            a1 = first[i]
            t1 = (second[i] - a1) % self.p2
            t1 = t1 * self.inverseP1ModP2 % self.p2
            combined12 = a1 + self.p1 * t1

            t2 = (third[i] - combined12 % self.p3) % self.p3
            t2 = t2 * self.inverseP12ModP3 % self.p3

            output[i] = (
                a1 % self.outputModulus
                + self.p1ModOutput * (t1 % self.outputModulus)
                + self.p12ModOutput * (t2 % self.outputModulus)
            ) % self.outputModulus

        return output


def buildB(limit, modulus, derivative, size):
    values = [0] * size

    for divisor in range(1, limit + 1):
        weightedDerivative = derivative[divisor] % modulus
        divisorMod = divisor % modulus
        power = weightedDerivative
        multiple = divisor

        while multiple <= limit:
            values[multiple] = (values[multiple] + divisorMod * power) % modulus
            power = power * weightedDerivative % modulus
            multiple += divisor

    return values


def computeG(limit, modulus=MOD):
    derivative = buildD(limit)
    size = nextPowerOfTwo(limit + 1)
    bValues = buildB(limit, modulus, derivative, size)
    inverses = modularInverses(limit, modulus)
    gValues = [0] * size
    convolutionValues = [0] * size
    convolver = NTTConvolver(bValues, modulus)
    threshold = 256

    def solveBlock(left, right):
        cappedRight = min(right, limit)
        for i in range(left, cappedRight + 1):
            if i == 0:
                current = 1
            else:
                current = convolutionValues[i] * inverses[i] % modulus
            gValues[i] = current

            maxOffset = cappedRight - i
            if maxOffset <= 0 or current == 0:
                continue
            for offset in range(1, maxOffset + 1):
                convolutionValues[i + offset] = (
                    convolutionValues[i + offset] + current * bValues[offset]
                ) % modulus

    def cdq(left, length):
        if left > limit:
            return
        right = left + length - 1
        if length <= threshold:
            solveBlock(left, right)
            return

        half = length // 2
        middle = left + half - 1
        cdq(left, half)

        if middle < limit:
            segment = gValues[left:middle + 1]
            conv = convolver.convolveFirstLength(segment, length)
            cappedRight = min(right, limit)
            for index in range(middle + 1, cappedRight + 1):
                convolutionValues[index] = (
                    convolutionValues[index] + conv[index - left]
                ) % modulus

        cdq(middle + 1, half)

    cdq(0, size)
    return gValues[:limit + 1]


def solve(limit=LIMIT):
    gValues = computeG(limit)
    return sum(gValues[1:limit + 1]) % MOD


def runTests():
    gValues = computeG(10)
    assert gValues[10] == 164
    assert sum(gValues[1:11]) % MOD == 396


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
