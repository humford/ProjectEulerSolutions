import time


TARGET_NUMERATOR = 15499
TARGET_DENOMINATOR = 94744


def primeGenerator():
    yield 2
    primes = [2]
    candidate = 3

    while True:
        is_prime = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(candidate)
            yield candidate

        candidate += 2


def totient(number):
    result = number
    reduced = number
    factor = 2

    while factor * factor <= reduced:
        if reduced % factor == 0:
            result = result // factor * (factor - 1)
            while reduced % factor == 0:
                reduced //= factor

        factor += 1 if factor == 2 else 2

    if reduced > 1:
        result = result // reduced * (reduced - 1)

    return result


def hasLowerResilience(denominator, target_numerator, target_denominator):
    return (
        totient(denominator) * target_denominator
        < target_numerator * (denominator - 1)
    )


def smallestResilientDenominator(target_numerator, target_denominator):
    primorial = 1

    for prime in primeGenerator():
        for multiplier in range(1, prime):
            candidate = primorial * multiplier
            if (
                candidate > 1
                and hasLowerResilience(candidate, target_numerator, target_denominator)
            ):
                return candidate

        primorial *= prime

    raise RuntimeError("unreachable")


def runTests():
    assert totient(12) == 4
    assert smallestResilientDenominator(4, 10) == 12


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = smallestResilientDenominator(TARGET_NUMERATOR, TARGET_DENOMINATOR)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
