import math
import time


MODULUS = 1_000_000_007


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)
    return [number for number, is_prime in enumerate(sieve) if is_prime]


def squareSubsetCount(start, end):
    size = end - start + 1
    remaining = list(range(start, end + 1))
    vectors = [0] * size
    prime_indices = {}

    def primeIndex(prime):
        if prime not in prime_indices:
            prime_indices[prime] = len(prime_indices)
        return prime_indices[prime]

    for prime in primesUpTo(math.isqrt(end)):
        first_multiple = ((start + prime - 1) // prime) * prime
        bit = 1 << primeIndex(prime)
        for multiple in range(first_multiple, end + 1, prime):
            index = multiple - start
            parity = 0
            while remaining[index] % prime == 0:
                remaining[index] //= prime
                parity ^= 1
            if parity:
                vectors[index] ^= bit

    for index, unfactored in enumerate(remaining):
        if unfactored > 1:
            vectors[index] ^= 1 << primeIndex(unfactored)

    basis = {}
    rank = 0
    for vector in vectors:
        while vector:
            leading_bit = vector.bit_length() - 1
            if leading_bit not in basis:
                basis[leading_bit] = vector
                rank += 1
                break
            vector ^= basis[leading_bit]

    return (pow(2, size - rank, MODULUS) - 1) % MODULUS


def runTests():
    assert squareSubsetCount(5, 10) == 3
    assert squareSubsetCount(40, 55) == 15
    assert squareSubsetCount(1_000, 1_234) == 975_523_611


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squareSubsetCount(1_000_000, 1_234_567)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
