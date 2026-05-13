import time
from bisect import bisect_right
from math import isqrt


def isPrime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def primesUpTo(limit):
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return [number for number in range(limit + 1) if sieve[number]]


def divisors(n):
    result = []
    for divisor in range(1, isqrt(n) + 1):
        if n % divisor == 0:
            result.append(divisor)
            if divisor * divisor != n:
                result.append(n // divisor)
    return sorted(result)


def primesCongruentToMinusOne(limit, modulus, smallPrimes):
    kLimit = (limit + 1) // modulus
    candidates = bytearray(b"\x01") * kLimit
    root = isqrt(limit)

    for prime in smallPrimes:
        if prime > root:
            break
        if prime == modulus:
            continue
        start = pow(modulus, -1, prime)
        minStart = (prime * prime + 1 + modulus - 1) // modulus
        if start < minStart:
            start += ((minStart - start + prime - 1) // prime) * prime
        if start <= kLimit:
            candidates[start - 1 : kLimit : prime] = b"\x00" * (((kLimit - start) // prime) + 1)

    return [modulus * k - 1 for k, isPrimeCandidate in enumerate(candidates, 1) if isPrimeCandidate]


def multiplicativeOrder(base, primeModulus, orderDivisors):
    residue = base % primeModulus
    if residue == 0:
        return None
    for order in orderDivisors:
        if pow(residue, order, primeModulus) == 1:
            return order
    raise ValueError("No multiplicative order found")


def badExponentOptions(prime, limit, divisor, orderDivisors):
    order = multiplicativeOrder(prime, divisor, orderDivisors)
    if order is None:
        return []

    maxExponent = 0
    power = 1
    while power * prime <= limit:
        power *= prime
        maxExponent += 1

    if order == 1:
        return [
            exponent
            for exponent in range(1, maxExponent + 1)
            if (exponent + 1) % divisor == 0
        ]
    return [
        exponent
        for exponent in range(1, maxExponent + 1)
        if (exponent + 1) % order == 0
    ]


def badPrimePowerEvents(limit, divisor):
    if not isPrime(divisor):
        raise ValueError("This solution uses the prime-divisor factorization of sigma(n).")

    smallPrimes = primesUpTo(isqrt(limit))
    orderDivisors = divisors(divisor - 1)
    events = []

    for prime in primesCongruentToMinusOne(limit, divisor, smallPrimes):
        events.append((prime, 1, prime))

    for prime in smallPrimes:
        if prime == divisor or prime % divisor == divisor - 1:
            continue
        for exponent in badExponentOptions(prime, limit, divisor, orderDivisors):
            events.append((prime, exponent, prime ** exponent))

    events.sort(key=lambda event: event[2])
    return events


def triangular(n):
    return n * (n + 1) // 2


def exactValuationSum(limit, event):
    prime, exponent, primePower = event
    quotientLimit = limit // primePower
    return primePower * (
        triangular(quotientLimit) - prime * triangular(quotientLimit // prime)
    )


def doubleExactValuationSum(limit, firstEvent, secondEvent):
    firstPrime, firstExponent, firstPower = firstEvent
    secondPrime, secondExponent, secondPower = secondEvent
    quotientLimit = limit // (firstPower * secondPower)
    return firstPower * secondPower * (
        triangular(quotientLimit)
        - firstPrime * triangular(quotientLimit // firstPrime)
        - secondPrime * triangular(quotientLimit // secondPrime)
        + firstPrime
        * secondPrime
        * triangular(quotientLimit // (firstPrime * secondPrime))
    )


def divisorSumDivisibilitySum(limit, divisor):
    events = badPrimePowerEvents(limit, divisor)
    if len(events) >= 3 and events[0][2] * events[1][2] * events[2][2] <= limit:
        raise ValueError("More than two bad prime-power events can coincide.")

    total = sum(exactValuationSum(limit, event) for event in events)
    primePowers = [event[2] for event in events]

    for index, event in enumerate(events):
        largestPartner = limit // event[2]
        if not primePowers or largestPartner < primePowers[0]:
            break
        for partnerIndex in range(index + 1, bisect_right(primePowers, largestPartner)):
            partner = events[partnerIndex]
            if event[0] != partner[0]:
                total -= doubleExactValuationSum(limit, event, partner)
    return total


def sigma(n):
    total = 0
    for divisor in range(1, n + 1):
        if n % divisor == 0:
            total += divisor
    return total


def runTests():
    assert sigma(4) == 7
    assert [n for n in range(1, 21) if sigma(n) % 7 == 0] == [4, 12, 13, 20]
    assert divisorSumDivisibilitySum(20, 7) == 49
    assert divisorSumDivisibilitySum(10 ** 6, 2_017) == 150_850_429
    assert divisorSumDivisibilitySum(10 ** 9, 2_017) == 249_652_238_344_557


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisorSumDivisibilitySum(10 ** 11, 2_017)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
