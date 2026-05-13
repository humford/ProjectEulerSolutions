from math import isqrt
import time


LIMIT = 2 * 10 ** 11


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0

    for number in range(2, isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start::number] = b"\x00" * (((limit - start) // number) + 1)

    return sieve, [number for number in range(2, limit + 1) if sieve[number]]


def isPrime(number, sieve):
    if number < len(sieve):
        return bool(sieve[number])
    if number < 2:
        return False

    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if number % prime == 0:
            return number == prime

    odd_part = number - 1
    twos = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        twos += 1

    for base in (2, 3, 5, 7, 11, 13, 17):
        if base >= number:
            continue

        value = pow(base, odd_part, number)
        if value == 1 or value == number - 1:
            continue

        for _ in range(twos - 1):
            value = value * value % number
            if value == number - 1:
                break
        else:
            return False

    return True


def factorize(number, primes):
    factors = []

    for prime in primes:
        if prime * prime > number:
            break

        if number % prime == 0:
            exponent = 0
            while number % prime == 0:
                number //= prime
                exponent += 1
            factors.append((prime, exponent))

    if number > 1:
        factors.append((number, 1))

    return factors


def divisorsFromFactors(factors):
    divisors = [1]

    for prime, exponent in factors:
        previous = divisors
        divisors = []
        power = 1

        for _ in range(exponent + 1):
            for divisor in previous:
                divisors.append(divisor * power)
            power *= prime

    return divisors


def totient(number, primes):
    result = number

    for prime, _ in factorize(number, primes):
        result = result // prime * (prime - 1)

    return result


def isCoresilient(number, primes):
    phi = totient(number, primes)
    return (number - 1) % (number - phi) == 0


def twoPrimeSolutions(limit, primes, sieve):
    result = set()

    for quotient in range(2, isqrt(limit) + 1, 2):
        kernel = quotient * quotient - quotient + 1

        for divisor in divisorsFromFactors(factorize(kernel, primes)):
            if divisor * divisor > kernel:
                continue

            smaller_prime = quotient + divisor
            larger_prime = quotient + kernel // divisor
            number = smaller_prime * larger_prime

            if (
                number <= limit
                and isPrime(smaller_prime, sieve)
                and isPrime(larger_prime, sieve)
            ):
                result.add(number)

    return result


def multiPrimeSolutions(limit, primes, sieve):
    odd_primes = [prime for prime in primes if prime > 2]
    result = set()

    def addLargestPrime(prefix, prefix_phi, largest_prefix_prime):
        non_coprime_count = prefix - prefix_phi
        maximum_prime = limit // prefix

        lower_quotient = (
            (largest_prefix_prime * prefix - 1)
            // (prefix_phi + largest_prefix_prime * non_coprime_count)
            + 1
        )
        upper_quotient = (maximum_prime * prefix - 1) // (
            prefix_phi + maximum_prime * non_coprime_count
        )

        for quotient in range(max(1, lower_quotient), upper_quotient + 1):
            denominator = prefix - quotient * non_coprime_count
            numerator = quotient * prefix_phi + 1
            if denominator <= 0 or numerator % denominator:
                continue

            largest_prime = numerator // denominator
            number = prefix * largest_prime
            if largest_prime <= largest_prefix_prime or number > limit:
                continue
            if isPrime(largest_prime, sieve):
                phi = prefix_phi * (largest_prime - 1)
                if (number - 1) % (number - phi) == 0:
                    result.add(number)

    def search(start_index, prefix, prefix_phi, prime_count):
        for index in range(start_index, len(odd_primes)):
            prime = odd_primes[index]
            if prefix * prime * prime > limit:
                break

            next_prefix = prefix * prime
            next_phi = prefix_phi * (prime - 1)
            if prime_count + 1 >= 2:
                addLargestPrime(next_prefix, next_phi, prime)
            search(index + 1, next_prefix, next_phi, prime_count + 1)

    search(0, 1, 1, 0)
    return result


def bruteCoresilienceSum(limit):
    sieve, primes = primeSieve(isqrt(limit))
    total = 0
    for number in range(4, limit + 1):
        if not isPrime(number, sieve) and isCoresilient(number, primes):
            total += number
    return total


def coresilienceSum(limit):
    sieve, primes = primeSieve(isqrt(limit))
    solutions = twoPrimeSolutions(limit, primes, sieve)
    solutions.update(multiPrimeSolutions(limit, primes, sieve))
    return sum(solutions)


def runTests():
    sieve, primes = primeSieve(100)
    assert totient(12, primes) == 4
    assert isCoresilient(15, primes)
    assert isCoresilient(85, primes)
    assert not isCoresilient(12, primes)
    assert coresilienceSum(10 ** 5) == bruteCoresilienceSum(10 ** 5)
    assert coresilienceSum(10 ** 8) == 5699973227


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = coresilienceSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
