from array import array
import time


MODULUS = 1_000_000_000
TWO_PART = 512
FIVE_PART = 5**9

TARGET_A = 12
TARGET_B = 345_678
TARGET_C = 9_012_345
TARGET_D = 678
TARGET_E = 90


def baseJumpTables(modulus, exponent, steps):
    base = array("I", [0]) * modulus
    for value in range(modulus):
        base[value] = (
            pow(value, exponent, modulus)
            * ((value + 1) % modulus)
            % modulus
        )

    tables = [base]
    for _ in range(1, (steps + 1).bit_length() + 1):
        previous = tables[-1]
        tables.append(array("I", (previous[previous[value]] for value in range(modulus))))

    return tables


class BaseTransformer:
    def __init__(self, jumpTables):
        self.jumpTables = jumpTables

    def __call__(self, value):
        return self.jumpTables[0][value]

    def iterate(self, value, count):
        bit = 0
        while count:
            if count & 1:
                value = self.jumpTables[bit][value]
            count //= 2
            bit += 1

        return value


class DTransformer:
    def __init__(self, previous, iterations, modulus):
        self.previous = previous
        self.iterations = iterations
        self.modulus = modulus
        self.callCache = {}
        self.jumpCache = {}

    def __call__(self, value):
        cached = self.callCache.get(value)
        if cached is not None:
            return cached

        start = value * self.previous(value) % self.modulus
        result = self.previous.iterate(start, self.iterations)
        self.callCache[value] = result
        return result

    def jump(self, bit, value):
        key = (bit, value)
        cached = self.jumpCache.get(key)
        if cached is not None:
            return cached

        if bit == 0:
            result = self(value)
        else:
            middle = self.jump(bit - 1, value)
            result = self.jump(bit - 1, middle)

        self.jumpCache[key] = result
        return result

    def iterate(self, value, count):
        bit = 0
        while count:
            if count & 1:
                value = self.jump(bit, value)
            count //= 2
            bit += 1

        return value


def transformedNumeralModulo(modulus, a, b, c, d):
    jumpTables = baseJumpTables(modulus, c, b + 1)
    transformer = DTransformer(BaseTransformer(jumpTables), b + 1, modulus)

    for _ in range(a):
        transformer = DTransformer(transformer, b, modulus)

    return transformer(d % modulus)


def chineseRemainder(twoResidue, fiveResidue):
    multiplier = ((fiveResidue - twoResidue) * pow(TWO_PART, -1, FIVE_PART)) % FIVE_PART
    return (twoResidue + TWO_PART * multiplier) % MODULUS


def F(a, b, c, d, e):
    twoResidue = transformedNumeralModulo(TWO_PART, a, b, c, d)
    fiveResidue = transformedNumeralModulo(FIVE_PART, a, b, c, d)
    numeral = chineseRemainder(twoResidue, fiveResidue)
    return (numeral + e) % MODULUS


def solve():
    return F(TARGET_A, TARGET_B, TARGET_C, TARGET_D, TARGET_E)


def runTests():
    assert F(1, 1, 1, 1, 0) == 399_885_292


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    assert answer == 547_480_666
    elapsed = time.time() - start

    print("Found " + str(answer).zfill(9) + " in " + str(elapsed) + " seconds.")
