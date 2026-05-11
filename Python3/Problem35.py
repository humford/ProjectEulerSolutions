def primeSieve(limit):
    is_prime = [True] * limit
    if limit > 0:
        is_prime[0] = False
    if limit > 1:
        is_prime[1] = False

    for value in range(2, int(limit ** 0.5) + 1):
        if is_prime[value]:
            for multiple in range(value * value, limit, value):
                is_prime[multiple] = False

    return is_prime


def rotations(n):
    digits = str(n)
    return [int(digits[index:] + digits[:index]) for index in range(len(digits))]


def isCircularPrime(n, primes):
    return all(primes[rotation] for rotation in rotations(n))


def circularPrimeCountBelow(limit):
    primes = primeSieve(limit)
    return sum(1 for value in range(limit) if primes[value] and isCircularPrime(value, primes))


def runTests():
    assert circularPrimeCountBelow(100) == 13


def solve():
    return circularPrimeCountBelow(1000000)


if __name__ == "__main__":
    runTests()
    print(solve())
