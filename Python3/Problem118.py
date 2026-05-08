import functools
import itertools
import time


def isPrime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True


def digitsFromMask(mask):
    return [str(index + 1) for index in range(9) if mask & (1 << index)]


def primesByMask():
    result = {}

    for mask in range(1, 1 << 9):
        primes = set()
        digits = digitsFromMask(mask)
        for permutation in itertools.permutations(digits):
            if len(permutation) > 1 and permutation[-1] in ("2", "4", "5", "6", "8"):
                continue
            number = int("".join(permutation))
            if isPrime(number):
                primes.add(number)
        result[mask] = sorted(primes)

    return result


def primeSetCount():
    primes = primesByMask()
    full_mask = (1 << 9) - 1

    @functools.lru_cache(maxsize=None)
    def count(remaining_mask, minimum_prime):
        if remaining_mask == 0:
            return 1

        total = 0
        submask = remaining_mask
        while submask:
            for prime in primes[submask]:
                if prime > minimum_prime:
                    total += count(remaining_mask ^ submask, prime)
            submask = (submask - 1) & remaining_mask
        return total

    return count(full_mask, 0)


def runTests():
    assert isPrime(2143)
    assert not isPrime(12345)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeSetCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
