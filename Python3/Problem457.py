import math
import time


PROBLEM_LIMIT = 10**7


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if isPrime[number]:
            start = number * number
            isPrime[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    return [number for number in range(2, limit + 1) if isPrime[number]]


def modularSquareRoot(number, prime):
    number %= prime
    if number == 0:
        return 0

    if pow(number, (prime - 1) // 2, prime) != 1:
        return None

    oddPart = prime - 1
    twoPower = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        twoPower += 1

    if twoPower == 1:
        return pow(number, (prime + 1) // 4, prime)

    nonResidue = 2
    while pow(nonResidue, (prime - 1) // 2, prime) != prime - 1:
        nonResidue += 1

    c = pow(nonResidue, oddPart, prime)
    x = pow(number, (oddPart + 1) // 2, prime)
    t = pow(number, oddPart, prime)
    m = twoPower

    while t != 1:
        i = 1
        tPower = t * t % prime
        while tPower != 1:
            tPower = tPower * tPower % prime
            i += 1

        b = pow(c, 1 << (m - i - 1), prime)
        c = b * b % prime
        x = x * b % prime
        t = t * c % prime
        m = i

    return x


def liftedRoot(root, prime):
    quotient = (root * root - 3 * root - 1) // prime
    derivative = (2 * root - 3) % prime
    correction = -quotient * pow(derivative, -1, prime) % prime
    return root + correction * prime


def R(prime):
    if prime in (2, 13):
        return 0

    sqrtDiscriminant = modularSquareRoot(13, prime)
    if sqrtDiscriminant is None:
        return 0

    inverseTwo = pow(2, -1, prime)
    roots = [
        (3 + sqrtDiscriminant) * inverseTwo % prime,
        (3 - sqrtDiscriminant) * inverseTwo % prime,
    ]
    liftedRoots = [liftedRoot(root, prime) for root in roots]

    return min(root for root in liftedRoots if root > 0)


def SR(limit):
    return sum(R(prime) for prime in primeSieve(limit))


def runTests():
    assert R(2) == 0
    assert R(5) == 0
    assert R(13) == 0
    assert R(29) == 272


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = SR(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
