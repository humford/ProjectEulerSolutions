import math
import time


LIMIT = 10**10


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


def totient(number):
    result = number
    remaining = number
    factor = 2

    while factor * factor <= remaining:
        if remaining % factor == 0:
            while remaining % factor == 0:
                remaining //= factor

            result -= result // factor

        factor += 1 if factor == 2 else 2

    if remaining > 1:
        result -= result // remaining

    return result


def isCube(number):
    root = round(number ** (1.0 / 3.0))

    while (root + 1) ** 3 <= number:
        root += 1

    while root**3 > number:
        root -= 1

    return root**3 == number


def bruteForceSum(limit):
    return sum(number for number in range(2, limit) if isCube(number * totient(number)))


def cubeTotientSum(limit=LIMIT):
    primes = primeSieve(math.isqrt(limit - 1))

    def search(index, number, phi):
        total = 0

        while True:
            while index >= 0:
                prime = primes[index]

                if phi % prime != 0 and number * prime * prime >= limit:
                    index -= 1
                else:
                    break

            if index < 0:
                return total + number

            prime = primes[index]
            exponentInPhi = 0
            reducedPhi = phi

            while reducedPhi % prime == 0:
                reducedPhi //= prime
                exponentInPhi += 1

            nextNumber = number
            exponent = 0

            while True:
                exponent += 1
                nextNumber *= prime

                if nextNumber >= limit:
                    break

                if (2 * exponent - 1 + exponentInPhi) % 3 == 0:
                    total += search(index - 1, nextNumber, phi * (prime - 1))

            if exponentInPhi % 3 != 0:
                return total

            index -= 1

    return search(len(primes) - 1, 1, 1) - 1


def runTests():
    assert cubeTotientSum(100) == bruteForceSum(100)
    assert cubeTotientSum(1000) == bruteForceSum(1000)
    assert isCube(50 * totient(50))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = cubeTotientSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
