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


def sumPrimesBelow(limit):
    return sum(value for value, prime in enumerate(primeSieve(limit)) if prime)


def runTests():
    assert sumPrimesBelow(10) == 17


def solve():
    return sumPrimesBelow(2000000)


if __name__ == "__main__":
    runTests()
    print(solve())
