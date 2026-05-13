import math
import time
from array import array


LIMIT = 2_000_000


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    if limit >= 4:
        sieve[4::2] = b"\x00" * ((limit - 4) // 2 + 1)

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start::step] = b"\x00" * ((limit - start) // step + 1)

    return [2] + [number for number in range(3, limit + 1, 2) if sieve[number]]


def tonelliShanks(number, prime):
    number %= prime

    if number == 0:
        return 0

    if prime % 4 == 3:
        return pow(number, (prime + 1) // 4, prime)

    q = prime - 1
    shift = 0

    while q % 2 == 0:
        shift += 1
        q //= 2

    nonResidue = 2
    while pow(nonResidue, (prime - 1) // 2, prime) != prime - 1:
        nonResidue += 1

    modulusPower = shift
    c = pow(nonResidue, q, prime)
    t = pow(number, q, prime)
    root = pow(number, (q + 1) // 2, prime)

    while t != 1:
        index = 1
        test = t * t % prime

        while test != 1:
            test = test * test % prime
            index += 1

        factor = pow(c, 1 << (modulusPower - index - 1), prime)
        modulusPower = index
        c = factor * factor % prime
        t = t * c % prime
        root = root * factor % prime

    return root


def largestPrimeFactor(number):
    largest = 1
    factor = 2

    while factor * factor <= number:
        if number % factor == 0:
            largest = factor

            while number % factor == 0:
                number //= factor

        factor += 1 if factor == 2 else 2

    return max(largest, number)


def fractionalSequenceValue(k):
    return largestPrimeFactor(k + 1) - 1


def fractionalSequenceCubeSum(limit=LIMIT):
    primes = primeSieve(limit + 1)
    factor1 = array("I", [0]) * (limit + 2)

    for prime in primes:
        for multiple in range(prime, limit + 2, prime):
            factor1[multiple] = prime

    quadratic = array("Q", [0]) * (limit + 1)
    factor2 = array("Q", [0]) * (limit + 1)

    for k in range(1, limit + 1):
        quadratic[k] = k * k - k + 1

    for prime in primes:
        if prime == 3:
            roots = [2]
        elif prime % 3 == 1:
            root = tonelliShanks(prime - 3, prime)
            inverse2 = (prime + 1) // 2
            roots = [
                ((1 + root) * inverse2) % prime,
                ((1 - root) * inverse2) % prime,
            ]
        else:
            continue

        for root in roots:
            if root == 0:
                root = prime

            for k in range(root, limit + 1, prime):
                if quadratic[k] % prime == 0:
                    factor2[k] = prime

                    while quadratic[k] % prime == 0:
                        quadratic[k] //= prime

    for k in range(1, limit + 1):
        if quadratic[k] > 1:
            factor2[k] = quadratic[k]

    return sum(max(factor1[k + 1], factor2[k]) - 1 for k in range(1, limit + 1))


def runTests():
    assert fractionalSequenceValue(1) == 1
    assert fractionalSequenceValue(2) == 2
    assert fractionalSequenceValue(3) == 1
    assert fractionalSequenceValue(20) == 6
    assert fractionalSequenceCubeSum(100) == 118937


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fractionalSequenceCubeSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
