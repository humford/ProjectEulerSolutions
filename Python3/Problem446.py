import time
from array import array
from math import isqrt


MODULUS = 1_000_000_007
PROBLEM_LIMIT = 10_000_000


def retractionCountFromFactorPowers(factorPowers):
    product = 1
    number = 1

    for primePower in factorPowers:
        product *= 1 + primePower
        number *= primePower

    return product - number


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"

    for number in range(2, isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    return [number for number in range(2, limit + 1) if sieve[number]]


def modularSquareRoot(number, prime):
    number %= prime
    if number == 0:
        return 0

    assert pow(number, (prime - 1) // 2, prime) == 1

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


def initializeFactors(limit):
    lowerFactors = array("Q", [0]) * (limit + 1)
    upperFactors = array("Q", [0]) * (limit + 1)
    products = array("I", [1]) * (limit + 1)

    for n in range(1, limit + 1):
        lowerFactors[n] = n * n - 2 * n + 2
        upperFactors[n] = n * n + 2 * n + 2

        if n % 2 == 0:
            lowerFactors[n] //= 2
            upperFactors[n] //= 2
            products[n] = 5

    return lowerFactors, upperFactors, products


def dividePrimeFromProgression(factors, products, prime, root, limit):
    if root == 0:
        root = prime

    for index in range(root, limit + 1, prime):
        value = factors[index]
        if value % prime == 0:
            primePower = 1
            while value % prime == 0:
                value //= prime
                primePower = primePower * prime % MODULUS

            factors[index] = value
            products[index] = products[index] * (primePower + 1) % MODULUS


def retractionPolynomialSum(limit):
    lowerFactors, upperFactors, products = initializeFactors(limit)

    # n^4+4=((n-1)^2+1)((n+1)^2+1).  Odd prime divisors of x^2+1
    # are exactly primes 1 mod 4, so roots of -1 mod p give sieve progressions.
    for prime in primeSieve(limit + 1):
        if prime == 2 or prime % 4 != 1:
            continue

        root = modularSquareRoot(prime - 1, prime)
        dividePrimeFromProgression(
            lowerFactors, products, prime, (1 + root) % prime, limit
        )
        dividePrimeFromProgression(
            lowerFactors, products, prime, (1 - root) % prime, limit
        )
        dividePrimeFromProgression(
            upperFactors, products, prime, (-1 + root) % prime, limit
        )
        dividePrimeFromProgression(
            upperFactors, products, prime, (-1 - root) % prime, limit
        )

    total = 0
    for n in range(1, limit + 1):
        product = products[n]

        if lowerFactors[n] > 1:
            product = product * (lowerFactors[n] % MODULUS + 1) % MODULUS
        if upperFactors[n] > 1:
            product = product * (upperFactors[n] % MODULUS + 1) % MODULUS

        total = (total + product - (pow(n, 4, MODULUS) + 4)) % MODULUS

    return total


def runTests():
    assert retractionCountFromFactorPowers([4, 3]) == 8
    assert retractionPolynomialSum(1_024) == 77_532_377_300_600 % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = retractionPolynomialSum(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
