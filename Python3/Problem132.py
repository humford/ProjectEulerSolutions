import time


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


def dividesRepunit(prime, exponent):
    if prime in (2, 5):
        return False
    if prime == 3:
        return exponent % 3 == 0
    return pow(10, exponent, prime) == 1


def repunitPrimeFactors(exponent, count):
    factors = []

    for prime in primeGenerator():
        if dividesRepunit(prime, exponent):
            factors.append(prime)
            if len(factors) == count:
                return factors

    raise ValueError("Unreachable")


def runTests():
    assert repunitPrimeFactors(10, 4) == [11, 41, 271, 9091]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sum(repunitPrimeFactors(10 ** 9, 40))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
