from array import array
import time


TARGET = 10_000_000


def polynomialProduct(a, b):
    product = 0
    while b:
        if b & 1:
            product ^= a
        a <<= 1
        b >>= 1
    return product


def polynomialRemainder(value, divisor):
    divisorDegree = divisor.bit_length() - 1
    while value.bit_length() - 1 >= divisorDegree:
        value ^= divisor << (value.bit_length() - divisor.bit_length())
    return value


def polynomialQuotientExact(value, divisor):
    quotient = 0
    divisorDegree = divisor.bit_length() - 1
    while value.bit_length() - 1 >= divisorDegree:
        shift = value.bit_length() - divisor.bit_length()
        quotient ^= 1 << shift
        value ^= divisor << shift
    return quotient


def irreduciblePolynomials(maxDegree):
    irreducibles = []
    for degree in range(1, maxDegree + 1):
        leading = 1 << degree
        for lowerBits in range(1 << degree):
            candidate = leading | lowerBits
            if degree > 1 and candidate & 1 == 0:
                continue

            reducible = False
            for divisor in irreducibles:
                if 2 * (divisor.bit_length() - 1) > degree:
                    break
                if polynomialRemainder(candidate, divisor) == 0:
                    reducible = True
                    break
            if not reducible:
                irreducibles.append(candidate)
    return irreducibles


def smallestFactorSieve(limit):
    maxDegree = limit.bit_length() - 1
    factors = array("I", [0]) * (limit + 1)

    for prime in irreduciblePolynomials(maxDegree // 2):
        quotientBits = maxDegree - (prime.bit_length() - 1) + 1
        multiple = 0
        previousGray = 0

        for index in range(1, 1 << quotientBits):
            gray = index ^ (index >> 1)
            changed = gray ^ previousGray
            multiple ^= prime << (changed.bit_length() - 1)
            if multiple <= limit and factors[multiple] == 0:
                factors[multiple] = prime
            previousGray = gray

    return factors


def toggledByX(squarefreeClass):
    if squarefreeClass & 1 == 0:
        return squarefreeClass >> 1
    return squarefreeClass << 1


def squarefreeClasses(limit):
    smallestFactor = smallestFactorSieve(limit)
    classes = array("I", [0]) * (limit + 1)
    classes[1] = 1

    for value in range(2, limit + 1):
        factor = smallestFactor[value]
        if factor == 0:
            classes[value] = value
            continue

        if factor == 2:
            quotient = value >> 1
            current = classes[quotient]
            classes[value] = current >> 1 if current & 1 == 0 else current << 1
            continue

        quotient = polynomialQuotientExact(value, factor)
        current = classes[quotient]
        if polynomialRemainder(current, factor) == 0:
            classes[value] = polynomialQuotientExact(current, factor)
        else:
            classes[value] = polynomialProduct(current, factor)

    return classes


def F(limit):
    classes = squarefreeClasses(limit)
    counts = array("I", [0]) * (1 << limit.bit_length())
    total = limit + 1

    for value in range(1, limit + 1):
        squarefreeClass = classes[value]
        target = toggledByX(squarefreeClass)
        if target < len(counts):
            total += counts[target]
        counts[squarefreeClass] += 1

    return total


def xorProduct(a, b):
    return polynomialProduct(a, b)


def isPolynomialSquare(value):
    return value & 0xAAAAAAAAAAAAAAAA == 0


def bruteF(limit):
    total = 0
    for a in range(limit + 1):
        for b in range(a, limit + 1):
            left = xorProduct(a, a) ^ xorProduct(2, xorProduct(a, b)) ^ xorProduct(b, b)
            if isPolynomialSquare(left):
                total += 1
    return total


def runTests():
    assert xorProduct(7, 3) == 9
    assert F(10) == 21
    for limit in range(1, 18):
        assert F(limit) == bruteF(limit)


def solve():
    return F(TARGET)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
