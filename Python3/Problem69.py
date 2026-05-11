def primeSieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    for value in range(2, int(limit ** 0.5) + 1):
        if is_prime[value]:
            for multiple in range(value * value, limit + 1, value):
                is_prime[multiple] = False

    return [value for value, prime in enumerate(is_prime) if prime]


def totientMaximum(limit):
    product = 1

    for prime in primeSieve(100):
        if product * prime > limit:
            return product
        product *= prime

    raise ValueError("Prime search bound was too small")


def runTests():
    assert totientMaximum(10) == 6


def solve():
    return totientMaximum(1000000)


if __name__ == "__main__":
    runTests()
    print(solve())
