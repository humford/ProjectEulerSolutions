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


def isTruncatablePrime(n, primes):
    if n < 10 or not primes[n]:
        return False

    digits = len(str(n))
    for power in range(1, digits):
        if not primes[n % (10 ** power)]:
            return False
        if not primes[n // (10 ** power)]:
            return False

    return True


def truncatablePrimes(limit):
    primes = primeSieve(limit)
    return [value for value in range(10, limit) if isTruncatablePrime(value, primes)]


def runTests():
    primes = primeSieve(10000)
    assert isTruncatablePrime(3797, primes)


def solve():
    return sum(truncatablePrimes(1000000))


if __name__ == "__main__":
    runTests()
    print(solve())
