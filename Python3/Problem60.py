import time
from functools import lru_cache


def primeSieve(limit):
    primes = [True] * limit
    primes[0] = False
    primes[1] = False

    for n in range(2, int(limit ** 0.5) + 1):
        if primes[n]:
            for multiple in range(n * n, limit, n):
                primes[multiple] = False

    return [n for n in range(limit) if primes[n]]


@lru_cache(maxsize=None)
def isPrime(n):
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    for prime in small_primes:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for base in (2, 3, 5, 7, 11):
        if base >= n:
            continue
        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


@lru_cache(maxsize=None)
def concatenate(a, b):
    scale = 10
    while scale <= b:
        scale *= 10
    return a * scale + b


@lru_cache(maxsize=None)
def pairCompatible(a, b):
    return isPrime(concatenate(a, b)) and isPrime(concatenate(b, a))


def lowestPrimePairSet(size, limit):
    primes = [prime for prime in primeSieve(limit) if prime not in (2, 5)]
    best_sum = None
    best_set = None

    def search(chosen, candidates, total):
        nonlocal best_sum, best_set

        if len(chosen) == size:
            best_sum = total
            best_set = chosen
            return

        remaining = size - len(chosen)
        for index, prime in enumerate(candidates):
            if best_sum is not None and total + prime * remaining >= best_sum:
                break

            next_candidates = [
                candidate
                for candidate in candidates[index + 1 :]
                if pairCompatible(prime, candidate)
            ]
            if len(next_candidates) >= remaining - 1:
                search(chosen + [prime], next_candidates, total + prime)

    search([], primes, 0)
    if best_set is None:
        raise ValueError("No set found below " + str(limit))
    return best_sum, best_set


def runTests():
    assert isPrime(673)
    assert pairCompatible(3, 7)
    assert pairCompatible(3, 109)
    assert pairCompatible(673, 109)
    assert lowestPrimePairSet(4, 1000) == (792, [3, 7, 109, 673])


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer, prime_set = lowestPrimePairSet(5, 30000)
    elapsed = time.time() - start

    print("Set " + str(prime_set))
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
