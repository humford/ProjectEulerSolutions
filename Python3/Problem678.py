import math
import time
from collections import Counter


TARGET = 10 ** 18


def integerRoot(number, exponent):
    if number < 2:
        return number

    root = int(round(number ** (1.0 / exponent)))
    while (root + 1) ** exponent <= number:
        root += 1
    while root ** exponent > number:
        root -= 1
    return root


def smallestPrimeFactors(limit):
    factors = list(range(limit + 1))
    root = math.isqrt(limit)
    for number in range(2, root + 1):
        if factors[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if factors[multiple] == multiple:
                    factors[multiple] = number
    return factors


def factorize(number, factors):
    result = {}
    while number > 1:
        prime = factors[number]
        count = 0
        while number % prime == 0:
            number //= prime
            count += 1
        result[prime] = count
    return result


def buildPerfectPowers(limit):
    multiplicities = Counter()
    representatives = {}
    exponentAtLeastFive = set()

    for exponent in range(3, 61):
        maxBase = integerRoot(limit, exponent)
        if maxBase < 2:
            break
        for base in range(2, maxBase + 1):
            value = pow(base, exponent)
            multiplicities[value] += 1
            representatives.setdefault(value, (base, exponent))
            if exponent >= 5:
                exponentAtLeastFive.add(value)

    return multiplicities, representatives, exponentAtLeastFive


def primePowersOfValue(value, representatives, factors):
    base, exponent = representatives[value]
    return [
        (prime, count * exponent)
        for prime, count in factorize(base, factors).items()
    ]


def countExponentTwo(multiplicities, representatives, factors):
    total = 0
    for value, multiplicity in multiplicities.items():
        base, exponent = representatives[value]
        product = 1
        possible = True

        for prime, count in factorize(base, factors).items():
            fullExponent = count * exponent
            if prime % 4 == 3 and fullExponent % 2 == 1:
                possible = False
                break
            if prime % 4 == 1:
                product *= fullExponent + 1

        if not possible:
            continue

        orderedIntegerRepresentations = 4 * product

        squareRoot = math.isqrt(value)
        axisRepresentations = 4 if squareRoot * squareRoot == value else 0

        diagonalRepresentations = 0
        if value % 2 == 0:
            halfRoot = math.isqrt(value // 2)
            if halfRoot * halfRoot == value // 2:
                diagonalRepresentations = 4

        positiveOrderedPairs = (
            orderedIntegerRepresentations
            - axisRepresentations
            - diagonalRepresentations
        ) // 8
        total += positiveOrderedPairs * multiplicity

    return total


def limitedDivisors(primePowers, limit):
    divisors = [1]
    for prime, exponent in primePowers:
        nextDivisors = []
        primePower = 1
        for _ in range(exponent + 1):
            for divisor in divisors:
                value = divisor * primePower
                if value <= limit:
                    nextDivisors.append(value)
            primePower *= prime
            if primePower > limit:
                break
        divisors = nextDivisors
    return divisors


def twoCubeRepresentationCount(value, primePowers):
    divisorLimit = 2 * integerRoot(value, 3)
    count = 0

    for totalBase in limitedDivisors(primePowers, divisorLimit):
        quotient = value // totalBase
        square = totalBase * totalBase

        if square <= quotient or (square - quotient) % 3 != 0:
            continue

        discriminantNumerator = 4 * quotient - square
        if discriminantNumerator <= 0 or discriminantNumerator % 3 != 0:
            continue

        discriminant = discriminantNumerator // 3
        root = math.isqrt(discriminant)
        if root * root != discriminant or (totalBase - root) % 2:
            continue

        a = (totalBase - root) // 2
        b = (totalBase + root) // 2
        if a > 0 and a < b and a ** 3 + b ** 3 == value:
            count += 1

    return count


def countExponentThree(multiplicities, representatives, factors):
    total = 0
    for value, multiplicity in multiplicities.items():
        cubeRoot = integerRoot(value, 3)
        if cubeRoot >= 2 and cubeRoot ** 3 == value:
            continue

        count = twoCubeRepresentationCount(
            value,
            primePowersOfValue(value, representatives, factors),
        )
        total += count * multiplicity

    return total


def fourthPowers(limit):
    maxBase = integerRoot(limit, 4)
    powers = [base ** 4 for base in range(1, maxBase + 1)]
    byValue = {value: base + 1 for base, value in enumerate(powers)}
    return powers, byValue


def countFourthPowerHighExponents(limit, multiplicities, exponentAtLeastFive):
    powers, byValue = fourthPowers(limit)
    total = 0

    for value in exponentAtLeastFive:
        fourthRoot = integerRoot(value, 4)
        if fourthRoot >= 2 and fourthRoot ** 4 == value:
            continue

        maxA = integerRoot(value - 1, 4)
        count = 0
        for a in range(1, maxA + 1):
            b = byValue.get(value - powers[a - 1])
            if b is not None and b > a:
                count += 1

        total += count * multiplicities[value]

    return total


def countFourthPowerCubesOnly(limit, multiplicities, excluded):
    maxBase = integerRoot(limit, 4)
    if maxBase < 2:
        return 0

    modulus = 8_645
    cubicResidues = [False] * modulus
    for value in range(modulus):
        cubicResidues[pow(value, 3, modulus)] = True

    fourthPower = [0] * (maxBase + 1)
    residueToBases = {}
    for base in range(1, maxBase + 1):
        value = base * base
        value *= value
        fourthPower[base] = value
        residue = value % modulus
        residueToBases.setdefault(residue, []).append(base)

    possibleResidues = sorted(residueToBases)
    candidatesByResidue = {}
    for residue in possibleResidues:
        candidates = []
        for otherResidue in possibleResidues:
            if cubicResidues[(residue + otherResidue) % modulus]:
                candidates.extend(residueToBases[otherResidue])
        candidatesByResidue[residue] = candidates

    total = 0
    for a in range(1, maxBase):
        aFourth = fourthPower[a]
        for b in candidatesByResidue[aFourth % modulus]:
            if b <= a:
                continue
            value = aFourth + fourthPower[b]
            if value > limit:
                continue
            cubeRoot = integerRoot(value, 3)
            if cubeRoot ** 3 == value and value not in excluded:
                total += multiplicities.get(value, 0)

    return total


def countExponentFour(limit, multiplicities, exponentAtLeastFive):
    return (
        countFourthPowerHighExponents(limit, multiplicities, exponentAtLeastFive)
        + countFourthPowerCubesOnly(limit, multiplicities, exponentAtLeastFive)
    )


def countLargeExponents(limit, multiplicities):
    total = 0
    for exponent in range(5, 61):
        maxBase = integerRoot(limit, exponent)
        if maxBase < 2:
            break

        powers = [base ** exponent for base in range(1, maxBase + 1)]
        for i in range(maxBase - 1):
            first = powers[i]
            for j in range(i + 1, maxBase):
                value = first + powers[j]
                if value > limit:
                    break
                total += multiplicities.get(value, 0)

    return total


def fermatLikeCount(limit):
    multiplicities, representatives, exponentAtLeastFive = buildPerfectPowers(limit)
    factors = smallestPrimeFactors(integerRoot(limit, 3))
    return (
        countExponentTwo(multiplicities, representatives, factors)
        + countExponentThree(multiplicities, representatives, factors)
        + countExponentFour(limit, multiplicities, exponentAtLeastFive)
        + countLargeExponents(limit, multiplicities)
    )


def runTests():
    assert 3 ** 3 + 6 ** 3 == 3 ** 5
    assert fermatLikeCount(10 ** 3) == 7
    assert fermatLikeCount(10 ** 5) == 53
    assert fermatLikeCount(10 ** 7) == 287


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fermatLikeCount(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
