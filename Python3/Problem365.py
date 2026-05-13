import math
import time


N = 10**18
K = 10**9
LOWER = 1000
UPPER = 5000


def primesBetween(lower, upper):
    sieve = bytearray(b"\x01") * upper
    sieve[0] = 0
    sieve[1] = 0

    for number in range(4, upper, 2):
        sieve[number] = 0

    for number in range(3, math.isqrt(upper - 1) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start:upper:step] = b"\x00" * ((upper - 1 - start) // step + 1)

    return [number for number in range(lower + 1, upper) if sieve[number]]


def lucasBinomial(n, k, prime):
    factorials = [1] * prime

    for number in range(1, prime):
        factorials[number] = factorials[number - 1] * number % prime

    inverseFactorials = [1] * prime
    inverseFactorials[prime - 1] = pow(factorials[prime - 1], prime - 2, prime)

    for number in range(prime - 1, 0, -1):
        inverseFactorials[number - 1] = inverseFactorials[number] * number % prime

    result = 1

    while n > 0 or k > 0:
        nDigit = n % prime
        kDigit = k % prime

        if kDigit > nDigit:
            return 0

        result = (
            result
            * factorials[nDigit]
            * inverseFactorials[kDigit]
            * inverseFactorials[nDigit - kDigit]
        ) % prime
        n //= prime
        k //= prime

    return result


def hugeBinomialSum():
    primes = primesBetween(LOWER, UPPER)
    residues = [lucasBinomial(N, K, prime) for prime in primes]
    total = 0

    for i in range(len(primes) - 2):
        p = primes[i]
        residueP = residues[i]

        for j in range(i + 1, len(primes) - 1):
            q = primes[j]
            pq = p * q
            valuePQ = residueP + p * (
                ((residues[j] - residueP) % q) * pow(p, -1, q) % q
            )

            for k in range(j + 1, len(primes)):
                r = primes[k]
                total += valuePQ + pq * (
                    ((residues[k] - valuePQ) % r) * pow(pq % r, -1, r) % r
                )

    return total


def runTests():
    assert lucasBinomial(10, 3, 7) == math.comb(10, 3) % 7


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hugeBinomialSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
