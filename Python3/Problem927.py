from math import isqrt
import time


TARGET_N = 10_000_000


def primeSieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, isqrt(limit) + 1):
        if isPrime[n]:
            isPrime[n * n:limit + 1:n] = b"\x00" * (((limit - n * n) // n) + 1)

    return [n for n in range(2, limit + 1) if isPrime[n]]


def distinctPrimeFactors(n, primes):
    factors = []

    for prime in primes:
        if prime * prime > n:
            break
        if n % prime == 0:
            factors.append(prime)
            while n % prime == 0:
                n //= prime

    if n > 1:
        factors.append(n)

    return factors


def hitsZeroForArity(modulus, arity):
    value = 1 % modulus
    seen = set()

    if arity == 2:
        while value not in seen:
            if value == 0:
                return True
            seen.add(value)
            value = (value * value + 1) % modulus
        return False

    while value not in seen:
        if value == 0:
            return True
        seen.add(value)
        value = (pow(value, arity, modulus) + 1) % modulus

    return False


def goodPrimeDivisors(limit):
    # For prime q, arities coprime to q-1 are covered once q is in S_2.
    # The only remaining prime arities to test are the prime divisors of q-1.
    primes = primeSieve(limit)
    good = []

    for prime in primes:
        if not hitsZeroForArity(prime, 2):
            continue

        if all(
            hitsZeroForArity(prime, factor)
            for factor in distinctPrimeFactors(prime - 1, primes)
        ):
            good.append(prime)

    return good


def squarefreeProducts(primes, limit):
    products = [1]

    for prime in primes:
        products.extend(
            product * prime
            for product in products[:]
            if product * prime <= limit
        )

    return products


def R(limit):
    return sum(squarefreeProducts(goodPrimeDivisors(limit), limit))


def solve():
    return R(TARGET_N)


def runTests():
    assert goodPrimeDivisors(20) == [2, 5]
    assert R(20) == 18
    assert R(1000) == 2089


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
