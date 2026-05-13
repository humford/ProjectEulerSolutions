import math
import time


MODULUS = 1_000_000_007


def primeFactors(number):
    factors = {}
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            number //= divisor
        divisor += 1 if divisor == 2 else 2
    if number > 1:
        factors[number] = factors.get(number, 0) + 1
    return factors


def divisorsFromFactors(factors):
    divisors = [1]
    for prime, exponent in factors.items():
        divisors = [
            divisor * primePower
            for divisor in divisors
            for primePower in (prime ** power for power in range(exponent + 1))
        ]
    return divisors


def totient(number):
    result = number
    for prime in primeFactors(number):
        result = result // prime * (prime - 1)
    return result


def dihedralCycleTypes(size):
    factors = primeFactors(size)
    cycleTypes = []

    for cycleLength in divisorsFromFactors(factors):
        cycleCount = size // cycleLength
        cycleTypes.append(({cycleLength: cycleCount}, totient(cycleLength)))

    if size % 2 == 1:
        cycleTypes.append(({1: 1, 2: (size - 1) // 2}, size))
    else:
        cycleTypes.append(({1: 2, 2: (size - 2) // 2}, size // 2))
        cycleTypes.append(({2: size // 2}, size // 2))

    return cycleTypes


def productCycleCount(firstCycleType, secondCycleType):
    return sum(
        firstCount * secondCount * math.gcd(firstLength, secondLength)
        for firstLength, firstCount in firstCycleType.items()
        for secondLength, secondCount in secondCycleType.items()
    )


def exactColoringCount(colors, cycles):
    total = 0
    for omitted in range(colors + 1):
        term = (
            math.comb(colors, omitted)
            * pow(colors - omitted, cycles, MODULUS)
        )
        if omitted % 2 == 0:
            total += term
        else:
            total -= term
    return total % MODULUS


def patternedCylinderCount(colors, axialPeriod, circumference):
    axialTypes = dihedralCycleTypes(axialPeriod)
    circumferenceTypes = dihedralCycleTypes(circumference)

    total = 0
    for axialCycleType, axialMultiplicity in axialTypes:
        for circumferenceCycleType, circumferenceMultiplicity in circumferenceTypes:
            cycles = productCycleCount(axialCycleType, circumferenceCycleType)
            total += (
                axialMultiplicity
                * circumferenceMultiplicity
                * exactColoringCount(colors, cycles)
            )
            total %= MODULUS

    groupSize = (4 * axialPeriod * circumference) % MODULUS
    return total * pow(groupSize, MODULUS - 2, MODULUS) % MODULUS


def fibonacciNumbers(limit):
    values = [0, 1]
    while len(values) <= limit:
        values.append(values[-1] + values[-2])
    return values


def patternedCylinderTotal():
    fibonacci = fibonacciNumbers(40)
    return sum(
        patternedCylinderCount(index, fibonacci[index - 1], fibonacci[index])
        for index in range(4, 41)
    ) % MODULUS


def runTests():
    assert patternedCylinderCount(2, 2, 3) == 11
    assert patternedCylinderCount(3, 2, 3) == 56
    assert patternedCylinderCount(2, 3, 4) == 156
    assert patternedCylinderCount(8, 13, 21) == 49_718_354
    assert patternedCylinderCount(13, 144, 233) == 907_081_451


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = patternedCylinderTotal() % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
