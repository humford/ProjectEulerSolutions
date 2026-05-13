from array import array
import math
import time


TARGET_ORDINAL = 100_000_000
LAST_DIGIT_MODULUS = 10**16
FIRST_13 = [1, 1, 2, 3, 5, 13, 21, 34, 55, 89, 233, 377, 610]


def smallestPrimeFactors(limit):
    smallestFactor = array("I", [0]) * (limit + 1)
    primes = array("I")

    for number in range(2, limit + 1):
        if smallestFactor[number] == 0:
            smallestFactor[number] = number
            primes.append(number)

        for prime in primes:
            product = number * prime

            if product > limit:
                break

            smallestFactor[product] = prime

            if prime == smallestFactor[number]:
                break

    return smallestFactor, primes


def factorization(number, smallestFactor):
    factors = []

    while number > 1:
        prime = smallestFactor[number]
        exponent = 0

        while number % prime == 0:
            number //= prime
            exponent += 1

        factors.append((prime, exponent))

    return factors


def limitedDivisors(factors, limit):
    divisors = [1]

    for prime, exponent in factors:
        nextDivisors = []
        power = 1

        for _ in range(exponent + 1):
            for divisor in divisors:
                value = divisor * power

                if value <= limit:
                    nextDivisors.append(value)

            power *= prime

        divisors = nextDivisors

    return sorted(divisors)


def fibonacciModulo(index, modulus):
    if index == 0:
        return 0, 1

    previous, current = fibonacciModulo(index // 2, modulus)
    doubled = previous * ((2 * current - previous) % modulus) % modulus
    squared = (previous * previous + current * current) % modulus

    if index % 2 == 1:
        return squared, (doubled + squared) % modulus

    return doubled, squared


def rankOfApparition(prime, smallestFactor, maxRank):
    if prime == 2:
        return 3

    if prime == 5:
        return 5

    legendreSymbol = pow(5, (prime - 1) // 2, prime)
    candidate = prime - 1 if legendreSymbol == 1 else prime + 1

    for divisor in limitedDivisors(factorization(candidate, smallestFactor), maxRank):
        if fibonacciModulo(divisor, prime)[0] == 0:
            return divisor

    return None


def forbiddenModuli(limit):
    maxPrime = limit // 3 + 2
    smallestFactor, primes = smallestPrimeFactors(maxPrime + 1)
    moduli = []

    for prime in primes:
        if prime > maxPrime:
            break

        maxRank = limit // prime

        if maxRank < 3:
            break

        rank = rankOfApparition(prime, smallestFactor, maxRank)

        if rank is None:
            continue

        modulus = prime * rank

        if modulus <= limit:
            moduli.append(modulus)

    reduced = []

    for modulus in sorted(set(moduli)):
        if not any(modulus % previous == 0 for previous in reduced):
            reduced.append(modulus)

    return reduced


def squarefreeIndexCount(limit, moduli):
    relevantModuli = [modulus for modulus in moduli if modulus <= limit]
    excluded = 0

    def search(startIndex, currentLcm, sign):
        nonlocal excluded

        for index in range(startIndex, len(relevantModuli)):
            nextLcm = currentLcm * relevantModuli[index] // math.gcd(
                currentLcm, relevantModuli[index]
            )

            if nextLcm > limit:
                continue

            excluded += sign * (limit // nextLcm)
            search(index + 1, nextLcm, -sign)

    search(0, 1, 1)
    return limit - excluded


def squarefreeFibonacciIndex(ordinal):
    high = ordinal * 4 // 3

    while True:
        moduli = forbiddenModuli(high)

        if squarefreeIndexCount(high, moduli) >= ordinal:
            break

        high *= 2

    low = 1

    while low < high:
        middle = (low + high) // 2

        if squarefreeIndexCount(middle, moduli) >= ordinal:
            high = middle
        else:
            low = middle + 1

    return low


def isSquarefree(number):
    divisor = 2

    while divisor * divisor <= number:
        if number % (divisor * divisor) == 0:
            return False

        divisor += 1

    return True


def firstSquarefreeFibonacciValues(count):
    values = []
    previous, current = 0, 1

    while len(values) < count:
        previous, current = current, previous + current

        if isSquarefree(previous):
            values.append(previous)

    return values


def scientificNotationForFibonacci(index):
    logValue = index * math.log10((1 + math.sqrt(5)) / 2) - math.log10(5) / 2
    exponent = math.floor(logValue)
    mantissa = round(10 ** (logValue - exponent), 1)

    if mantissa >= 10:
        mantissa = 1.0
        exponent += 1

    return f"{mantissa:.1f}e{exponent}"


def answer(ordinal=TARGET_ORDINAL):
    index = squarefreeFibonacciIndex(ordinal)
    lastDigits = fibonacciModulo(index, LAST_DIGIT_MODULUS)[0]
    return f"{lastDigits:016d},{scientificNotationForFibonacci(index)}"


def runTests():
    assert firstSquarefreeFibonacciValues(13) == FIRST_13
    assert squarefreeFibonacciIndex(200) == 260
    assert answer(200) == "1608739584170445,9.7e53"


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = answer()
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")
