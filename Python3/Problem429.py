import time


LIMIT = 100_000_000
MODULUS = 1_000_000_009


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[:2] = b"\x00\x00"

    for number in range(2, int(limit**0.5) + 1):
        if isPrime[number]:
            start = number * number
            isPrime[start : limit + 1 : number] = b"\x00" * (
                ((limit - start) // number) + 1
            )

    return isPrime


def factorialPrimeExponent(limit, prime):
    exponent = 0

    while limit:
        limit //= prime
        exponent += limit

    return exponent


def unitarySquareSum(limit=LIMIT):
    isPrime = primeSieve(limit)
    total = 1

    for prime in range(2, limit + 1):
        if isPrime[prime]:
            exponent = factorialPrimeExponent(limit, prime)
            total = total * (1 + pow(prime, 2 * exponent, MODULUS)) % MODULUS

    return total


def runTests():
    assert unitarySquareSum(4) == 650
    assert unitarySquareSum(10) == 683631060


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = unitarySquareSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
