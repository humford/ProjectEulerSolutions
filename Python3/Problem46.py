from math import isqrt


def primeSieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    for value in range(2, isqrt(limit) + 1):
        if is_prime[value]:
            for multiple in range(value * value, limit + 1, value):
                is_prime[multiple] = False

    return is_prime


def fitsGoldbachOtherConjecture(n, primes):
    for prime, is_prime in enumerate(primes[:n]):
        if is_prime:
            square = (n - prime) // 2
            root = isqrt(square)
            if prime + 2 * root * root == n:
                return True
    return False


def smallestOddCompositeFailure(limit):
    primes = primeSieve(limit)
    for value in range(9, limit + 1, 2):
        if not primes[value] and not fitsGoldbachOtherConjecture(value, primes):
            return value
    raise ValueError("No failure found below %s" % limit)


def runTests():
    primes = primeSieve(100)
    assert fitsGoldbachOtherConjecture(33, primes)


def solve():
    return smallestOddCompositeFailure(10000)


if __name__ == "__main__":
    runTests()
    print(solve())
