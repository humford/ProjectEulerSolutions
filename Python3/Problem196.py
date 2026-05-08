import math
import time


def triangleNumberAt(position, row):
    return row * (row - 1) // 2 + position


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                (limit - start) // number + 1
            )

    return [number for number in range(limit + 1) if sieve[number]]


def primeSegment(low, high, base_primes):
    segment = bytearray(b"\x01") * (high - low + 1)

    if low == 1:
        segment[0] = 0

    for prime in base_primes:
        if prime * prime > high:
            break

        start = max(prime * prime, ((low + prime - 1) // prime) * prime)
        segment[start - low : high - low + 1 : prime] = b"\x00" * (
            (high - start) // prime + 1
        )

    return segment


def primeTripletSum(row, base_primes=None):
    low = triangleNumberAt(1, max(1, row - 2))
    high = triangleNumberAt(row + 2, row + 2)

    if base_primes is None:
        base_primes = primesUpTo(math.isqrt(high))

    segment = primeSegment(low, high, base_primes)

    def isPrime(position, check_row):
        if check_row < 1 or position < 1 or position > check_row:
            return False

        number = triangleNumberAt(position, check_row)
        return segment[number - low] == 1

    three_plus = set()
    for check_row in range(max(1, row - 1), row + 2):
        for position in range(1, check_row + 1):
            if not isPrime(position, check_row):
                continue

            prime_count = 0
            for delta_row in (-1, 0, 1):
                for delta_position in (-1, 0, 1):
                    if isPrime(position + delta_position, check_row + delta_row):
                        prime_count += 1
                        if prime_count >= 3:
                            three_plus.add((position, check_row))
                            break
                if prime_count >= 3:
                    break

    total = 0
    for position in range(1, row + 1):
        if not isPrime(position, row):
            continue

        for delta_row in (-1, 0, 1):
            if any(
                (position + delta_position, row + delta_row) in three_plus
                for delta_position in (-1, 0, 1)
            ):
                total += triangleNumberAt(position, row)
                break

    return total


def runTests():
    assert primeTripletSum(8) == 60
    assert primeTripletSum(9) == 37
    assert primeTripletSum(10000) == 950007619


if __name__ == "__main__":
    runTests()
    start = time.time()
    max_high = triangleNumberAt(7208785 + 2, 7208785 + 2)
    base_primes = primesUpTo(math.isqrt(max_high))
    answer = primeTripletSum(5678027, base_primes) + primeTripletSum(
        7208785, base_primes
    )
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
