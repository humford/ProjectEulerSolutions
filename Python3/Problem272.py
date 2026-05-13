import math
import time


LIMIT = 10**11
TARGET_ROOTS = 242


def primeSieve(limit):
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    if limit >= 4:
        sieve[4 : limit + 1 : 2] = b"\x00" * ((limit - 4) // 2 + 1)

    for number in range(3, math.isqrt(limit) + 1, 2):
        if sieve[number]:
            step = 2 * number
            start = number * number
            sieve[start : limit + 1 : step] = b"\x00" * (
                (limit - start) // step + 1
            )

    return [2] + [number for number in range(3, limit + 1, 2) if sieve[number]]


def bruteCubeRootCount(modulus):
    return sum(1 for value in range(2, modulus) if pow(value, 3, modulus) == 1)


def inertPrefixSums(limit):
    primes = primeSieve(limit)
    allow_one_three = bytearray(b"\x01") * (limit + 1)
    allow_one_three[0] = 0

    if limit >= 9:
        allow_one_three[9 : limit + 1 : 9] = b"\x00" * ((limit - 9) // 9 + 1)

    for prime in primes:
        if prime % 3 == 1:
            allow_one_three[prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime) // prime + 1
            )

    no_three = allow_one_three[:]
    if limit >= 3:
        no_three[3 : limit + 1 : 3] = b"\x00" * ((limit - 3) // 3 + 1)

    prefix_allow = [0] * (limit + 1)
    prefix_no_three = [0] * (limit + 1)
    total_allow = 0
    total_no_three = 0

    for number in range(1, limit + 1):
        if allow_one_three[number]:
            total_allow += number
        if no_three[number]:
            total_no_three += number
        prefix_allow[number] = total_allow
        prefix_no_three[number] = total_no_three

    return prefix_allow, prefix_no_three


def modularCubePart2Sum(limit):
    max_good_prime = limit // (9 * 7 * 13 * 19)
    primes = [prime for prime in primeSieve(max_good_prime) if prime % 3 == 1]
    prime_count = len(primes)

    minimum_good_part = 9 * 7 * 13 * 19 * 31
    prefix_allow, prefix_no_three = inertPrefixSums(limit // minimum_good_part)

    minimum_product = [[1] * (prime_count + 1) for _ in range(6)]
    for count in range(1, 6):
        minimum_product[count][prime_count] = limit + 1

    for index in range(prime_count - 1, -1, -1):
        for count in range(1, 6):
            value = primes[index] * minimum_product[count - 1][index + 1]
            minimum_product[count][index] = value if value <= limit else limit + 1

    def sumPick(remaining, prefix, initial_product=1):
        total = 0

        def search(start, picks_left, product):
            nonlocal total

            if picks_left == 1:
                max_factor = limit // product
                for index in range(start, prime_count):
                    prime = primes[index]
                    if prime > max_factor:
                        break

                    power = prime
                    while power <= max_factor:
                        good_part = product * power
                        total += good_part * prefix[limit // good_part]
                        power *= prime
                return

            last = prime_count - picks_left
            for index in range(start, last + 1):
                prime = primes[index]
                if (
                    product
                    * prime
                    * minimum_product[picks_left - 1][index + 1]
                    > limit
                ):
                    break

                max_power = limit // (
                    product * minimum_product[picks_left - 1][index + 1]
                )
                power = prime
                while power <= max_power:
                    search(index + 1, picks_left - 1, product * power)
                    power *= prime

        search(0, remaining, initial_product)
        return total

    total = sumPick(5, prefix_allow)
    power_of_three = 9

    while power_of_three * minimum_product[4][0] <= limit:
        total += sumPick(4, prefix_no_three, power_of_three)
        power_of_three *= 3

    return total


def runTests():
    assert bruteCubeRootCount(91) == 8


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = modularCubePart2Sum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
