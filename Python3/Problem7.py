import math


def primeSieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    for value in range(2, int(limit ** 0.5) + 1):
        if is_prime[value]:
            for multiple in range(value * value, limit + 1, value):
                is_prime[multiple] = False

    return [value for value, prime in enumerate(is_prime) if prime]


def upperPrimeBound(n):
    if n < 6:
        return 15
    return math.ceil(n * (math.log(n) + math.log(math.log(n))))


def nthPrime(n):
    return primeSieve(upperPrimeBound(n))[n - 1]


def runTests():
    assert nthPrime(6) == 13


def solve():
    return nthPrime(10001)


if __name__ == "__main__":
    runTests()
    print(solve())
