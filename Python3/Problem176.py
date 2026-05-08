import time


PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def squareDivisorCount(number):
    remaining = number
    divisor_count = 1
    factor = 2

    while factor * factor <= remaining:
        exponent = 0
        while remaining % factor == 0:
            remaining //= factor
            exponent += 1
        if exponent:
            divisor_count *= 2 * exponent + 1
        factor += 1 if factor == 2 else 2

    if remaining > 1:
        divisor_count *= 3

    return divisor_count


def triangleCount(cathetus):
    if cathetus % 2 == 0:
        return (squareDivisorCount(cathetus // 2) - 1) // 2
    return (squareDivisorCount(cathetus) - 1) // 2


def oddDivisors(number):
    return [divisor for divisor in range(3, number + 1, 2) if number % divisor == 0]


def minimumWithSquareDivisorCount(required, primes, prime_index=0, max_factor=None):
    if required == 1:
        return 1

    if max_factor is None:
        max_factor = required

    best = None
    for factor in oddDivisors(required):
        if factor > max_factor:
            continue

        exponent = (factor - 1) // 2
        rest = minimumWithSquareDivisorCount(
            required // factor, primes, prime_index + 1, factor
        )
        if rest is None:
            continue

        candidate = primes[prime_index] ** exponent * rest
        if best is None or candidate < best:
            best = candidate

    return best


def smallestCathetusWithCount(target_count):
    required_divisors = 2 * target_count + 1
    even_cathetus = 2 * minimumWithSquareDivisorCount(required_divisors, PRIMES)
    odd_cathetus = minimumWithSquareDivisorCount(required_divisors, PRIMES[1:])

    return min(even_cathetus, odd_cathetus)


def runTests():
    assert triangleCount(12) == 4
    assert smallestCathetusWithCount(4) == 12


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = smallestCathetusWithCount(47547)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
