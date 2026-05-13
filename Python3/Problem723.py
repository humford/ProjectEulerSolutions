import math
import time


TARGET = 1_411_033_124_176_203_125
ODD_PRIMES = [5, 13, 17, 29, 37, 41, 53, 61]
TARGET_FACTORIZATION = {
    5: 6,
    13: 3,
    17: 2,
    29: 1,
    37: 1,
    41: 1,
    53: 1,
    61: 1,
}


def gaussianMultiply(left, right):
    x, y = left
    u, v = right
    return x * u - y * v, x * v + y * u


def unitMultiples(value):
    x, y = value
    return [(x, y), (-y, x), (-x, -y), (y, -x)]


def sqrtMinusOneModPrime(prime):
    exponent = (prime - 1) // 4
    for base in range(2, prime):
        value = pow(base, exponent, prime)
        if value * value % prime == prime - 1:
            return value
    raise ValueError("missing square root of -1")


def twoSquarePrimeRepresentation(prime):
    previous, current = prime, sqrtMinusOneModPrime(prime)
    while current * current > prime:
        previous, current = current, previous % current

    a = current
    bSquared = prime - a * a
    b = math.isqrt(bSquared)
    if b * b != bSquared:
        raise ValueError("Cornacchia failed")
    if a > b:
        a, b = b, a
    return a, b


def divisorsFromFactorization(factorization):
    divisors = [1]
    for prime, exponent in factorization.items():
        nextDivisors = []
        primePower = 1
        for _ in range(exponent + 1):
            for divisor in divisors:
                nextDivisors.append(divisor * primePower)
            primePower *= prime
        divisors = nextDivisors
    return divisors


def factorWithKnownPrimes(number):
    factorization = {}
    for prime in ODD_PRIMES:
        exponent = 0
        while number % prime == 0:
            number //= prime
            exponent += 1
        if exponent:
            factorization[prime] = exponent
    if number != 1:
        raise ValueError("number has a prime outside the configured target factorization")
    return factorization


def exponentTuple(number):
    exponent2 = 0
    while number % 2 == 0:
        number //= 2
        exponent2 += 1

    oddExponents = []
    for prime in ODD_PRIMES:
        exponent = 0
        while number % prime == 0:
            number //= prime
            exponent += 1
        oddExponents.append(exponent)

    if number != 1:
        raise ValueError("unexpected prime factor")
    return exponent2, tuple(oddExponents)


def r2FromExponents(exponent2, oddExponents):
    product = 1
    for exponent in oddExponents:
        product *= exponent + 1
    return 4 * product


def primitiveR2FromExponents(exponent2, oddExponents):
    squarePrimeIndexes = [
        index for index, exponent in enumerate(oddExponents) if exponent >= 2
    ]

    total = 0
    for mask in range(1 << len(squarePrimeIndexes)):
        exponents = list(oddExponents)
        sign = -1 if mask.bit_count() & 1 else 1
        for bit, index in enumerate(squarePrimeIndexes):
            if (mask >> bit) & 1:
                exponents[index] -= 2
        total += sign * r2FromExponents(exponent2, exponents)

    return total


GAUSSIAN_BASE = {
    prime: twoSquarePrimeRepresentation(prime) for prime in ODD_PRIMES
}

PRIME_POWER_CLASSES = {2: {0: [(1, 0)], 1: [(1, 1)]}}
for prime in ODD_PRIMES:
    PRIME_POWER_CLASSES[prime] = {0: [(1, 0)]}
    base = GAUSSIAN_BASE[prime]
    conjugate = (base[0], -base[1])
    for exponent in range(1, TARGET_FACTORIZATION[prime] + 1):
        basePowers = [(1, 0)]
        conjugatePowers = [(1, 0)]
        for _ in range(exponent):
            basePowers.append(gaussianMultiply(basePowers[-1], base))
            conjugatePowers.append(gaussianMultiply(conjugatePowers[-1], conjugate))

        classes = []
        for split in range(exponent + 1):
            classes.append(gaussianMultiply(basePowers[split], conjugatePowers[exponent - split]))
        PRIME_POWER_CLASSES[prime][exponent] = classes


def gaussianClasses(exponent2, oddExponents):
    classes = [(1, 0)]
    if exponent2 == 1:
        classes = [gaussianMultiply(value, (1, 1)) for value in classes]

    for index, prime in enumerate(ODD_PRIMES):
        exponent = oddExponents[index]
        if exponent == 0:
            continue

        nextClasses = []
        for current in classes:
            for primePowerClass in PRIME_POWER_CLASSES[prime][exponent]:
                nextClasses.append(gaussianMultiply(current, primePowerClass))
        classes = nextClasses

    return classes


Q_CACHE = {}


def plainDiagonalPairCount(exponent2, oddExponents):
    value = 2**exponent2
    for index, prime in enumerate(ODD_PRIMES):
        value *= prime ** oddExponents[index]

    if value in Q_CACHE:
        return Q_CACHE[value]

    xCounts = {}
    for gaussianClass in gaussianClasses(exponent2, oddExponents):
        for x, y in unitMultiples(gaussianClass):
            if y > 0 and x != 0:
                xAbs = abs(x)
                xCounts[xAbs] = xCounts.get(xAbs, 0) + 1

    if not xCounts:
        Q_CACHE[value] = 0
        return 0

    items = sorted((x * x, count) for x, count in xCounts.items())
    squares = [square for square, _ in items]
    weights = [count for _, count in items]
    prefixWeights = []
    running = 0
    for weight in weights:
        running += weight
        prefixWeights.append(running)

    total = 0
    right = len(items) - 1
    for left, square in enumerate(squares):
        while right >= 0 and square + squares[right] >= value:
            right -= 1
        if right < 0:
            break
        total += weights[left] * prefixWeights[right]

    Q_CACHE[value] = total
    return total


def allDivisorsFromExponents(exponent2, oddExponents):
    divisors = []
    for exponent2Part in range(exponent2 + 1):
        divisors.append((exponent2Part, [0] * len(oddExponents), 2**exponent2Part))

    for index, prime in enumerate(ODD_PRIMES):
        exponentMax = oddExponents[index]
        if exponentMax == 0:
            continue

        nextDivisors = []
        for currentExponent2, exponents, value in divisors:
            primePower = 1
            for exponent in range(exponentMax + 1):
                nextExponents = exponents[:]
                nextExponents[index] = exponent
                nextDivisors.append(
                    (currentExponent2, nextExponents, value * primePower)
                )
                primePower *= prime
        divisors = nextDivisors

    return divisors


def pythagoreanQuadrilateralCountSquared(radiusSquared):
    exponent2, oddExponents = exponentTuple(radiusSquared)
    pointCount = r2FromExponents(exponent2, oddExponents)
    halfPoints = pointCount // 2
    diameterCount = halfPoints * (halfPoints - 1) * (2 * halfPoints - 3) // 2

    total = 0
    lExponent2, lOddExponents = exponentTuple(4 * radiusSquared)
    for lExp2, lOddExps, lValue in allDivisorsFromExponents(lExponent2, lOddExponents):
        primitiveDirections = primitiveR2FromExponents(lExp2, tuple(lOddExps)) // 2
        if primitiveDirections == 0:
            continue

        quotient = 4 * radiusSquared // lValue
        if lValue & 1:
            if quotient % 4 != 0:
                continue
            qExp2, qOddExps = exponentTuple(quotient // 4)
        else:
            if quotient & 1:
                continue
            qExp2, qOddExps = exponentTuple(quotient)

        total += primitiveDirections * plainDiagonalPairCount(qExp2, qOddExps)

    return diameterCount + total // 2


def optimizedTargetSum():
    divisors = divisorsFromFactorization(TARGET_FACTORIZATION)
    divisors.sort()
    divisorExponents = {divisor: exponentTuple(divisor) for divisor in divisors}

    qOdd = {}
    qEven = {}
    for divisor in divisors:
        _, oddExponents = divisorExponents[divisor]
        qOdd[divisor] = plainDiagonalPairCount(0, oddExponents)
        qEven[divisor] = plainDiagonalPairCount(1, oddExponents)

    oddPrefix = {divisor: 0 for divisor in divisors}
    evenPrefix = {divisor: 0 for divisor in divisors}
    for divisor in divisors:
        _, divisorOddExponents = divisorExponents[divisor]
        oddTotal = 0
        evenTotal = 0
        for subDivisor in divisors:
            if subDivisor > divisor:
                break
            _, subOddExponents = divisorExponents[subDivisor]
            if all(
                subOddExponents[index] <= divisorOddExponents[index]
                for index in range(len(ODD_PRIMES))
            ):
                oddTotal += qOdd[subDivisor]
                evenTotal += qEven[subDivisor]
        oddPrefix[divisor] = oddTotal
        evenPrefix[divisor] = evenTotal

    diameterSum = 0
    for divisor in divisors:
        exp2, oddExponents = divisorExponents[divisor]
        pointCount = r2FromExponents(exp2, oddExponents)
        halfPoints = pointCount // 2
        diameterSum += halfPoints * (halfPoints - 1) * (2 * halfPoints - 3) // 2

    nonDiameterTwice = 0
    for divisor in divisors:
        exp2, oddExponents = divisorExponents[divisor]
        primitiveOdd = primitiveR2FromExponents(exp2, oddExponents) // 2
        primitiveEven = primitiveR2FromExponents(1, oddExponents) // 2
        quotient = TARGET // divisor
        nonDiameterTwice += (
            primitiveOdd * oddPrefix[quotient]
            + primitiveEven * evenPrefix[quotient]
        )

    return diameterSum + nonDiameterTwice // 2


def pythagoreanQuadrilateralSum(number):
    if number == TARGET:
        return optimizedTargetSum()

    factorization = factorWithKnownPrimes(number)
    return sum(
        pythagoreanQuadrilateralCountSquared(divisor)
        for divisor in divisorsFromFactorization(factorization)
    )


def runTests():
    assert pythagoreanQuadrilateralCountSquared(1) == 1
    assert pythagoreanQuadrilateralCountSquared(2) == 1
    assert pythagoreanQuadrilateralCountSquared(5) == 38
    assert pythagoreanQuadrilateralCountSquared(25) == 167
    assert pythagoreanQuadrilateralSum(325) == 2_370
    assert pythagoreanQuadrilateralSum(1_105) == 5_535


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pythagoreanQuadrilateralSum(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
