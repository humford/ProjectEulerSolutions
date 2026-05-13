import math
import time


GOOD_RESIDUES = (1, 25, 121)
MODULUS = 168


def smallPrimes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    return [number for number in range(3, limit + 1, 2) if sieve[number]]


def allowedPrimes(limit):
    base_primes = smallPrimes(math.isqrt(limit))
    primes = []
    segment_size = 50000000

    for low in range(2, limit + 1, segment_size):
        high = min(limit + 1, low + segment_size)
        segment = bytearray(b"\x01") * (high - low)
        if low == 2:
            segment[0] = 0

        for prime in base_primes:
            square = prime * prime
            if square >= high:
                break

            start = max(square, ((low + prime - 1) // prime) * prime)
            segment[start - low : high - low : prime] = b"\x00" * (
                (high - start - 1) // prime + 1
            )

        for residue in GOOD_RESIDUES:
            first = low + ((residue - low) % MODULUS)
            for prime in range(first, high, MODULUS):
                if segment[prime - low]:
                    primes.append(prime)

    primes.sort()
    return primes


def squarefreeKernelCount(limit):
    primes = allowedPrimes(limit)
    total = 0

    def search(start_index, product):
        nonlocal total
        total += math.isqrt(limit // product)

        max_prime = limit // product
        index = start_index
        while index < len(primes) and primes[index] <= max_prime:
            search(index + 1, product * primes[index])
            index += 1

    search(0, 1)
    return total


def smallestPrimeFactors(limit):
    spf = list(range(limit + 1))
    spf[0] = 0
    spf[1] = 1

    for number in range(2, math.isqrt(limit) + 1):
        if spf[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if spf[multiple] == multiple:
                    spf[multiple] = number

    return spf


def badSquareCount(limit):
    root = math.isqrt(limit)
    spf = smallestPrimeFactors(root)
    bad = 0

    for square_root in range(1, root + 1):
        remaining = square_root
        sum_two_squares = False
        sum_two_square_two = False
        sum_two_square_three = False
        sum_two_square_seven = False

        while remaining > 1:
            prime = spf[remaining]
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1

            if prime % 4 == 1:
                sum_two_squares = True
            if prime % 8 in (1, 3):
                sum_two_square_two = True
            if prime == 2 or prime % 3 == 1:
                sum_two_square_three = True
            if prime % 28 in (1, 9, 11, 15, 23, 25) or (
                prime == 2 and exponent >= 2
            ):
                sum_two_square_seven = True

        if not (
            sum_two_squares
            and sum_two_square_two
            and sum_two_square_three
            and sum_two_square_seven
        ):
            bad += 1

    return bad


def representationCount(limit):
    return squarefreeKernelCount(limit) - badSquareCount(limit)


def runTests():
    assert representationCount(10 ** 7) == 75373


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = representationCount(2 * 10 ** 9)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
