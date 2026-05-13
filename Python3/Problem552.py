import math
import time


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (
                ((limit - start) // number) + 1
            )
    return [number for number in range(limit + 1) if sieve[number]]


def chineseLeftoverA(n):
    primes = primeSieve(n * (math.ceil(math.log(n + 1)) + 2))
    solution = 0
    modulus = 1
    for index, prime in enumerate(primes[:n], start=1):
        step = ((index - solution) * pow(modulus, -1, prime)) % prime
        solution += modulus * step
        modulus *= prime
    return solution


def primeDivisorSum(limit):
    primes = primeSieve(limit)
    primeCount = len(primes)

    # For each future prime q, store A_n and p_1...p_n modulo q.
    residues = [1 % prime for prime in primes]
    moduli = [2 % prime for prime in primes]
    dividesSomeA = [False] * primeCount

    for currentIndex in range(1, primeCount):
        currentPrime = primes[currentIndex]
        n = currentIndex + 1
        step = (
            (n - residues[currentIndex])
            * pow(moduli[currentIndex], -1, currentPrime)
        ) % currentPrime

        for futureIndex in range(currentIndex + 1, primeCount):
            futurePrime = primes[futureIndex]
            residues[futureIndex] = (
                residues[futureIndex] + step * moduli[futureIndex]
            ) % futurePrime
            moduli[futureIndex] = (
                moduli[futureIndex] * currentPrime
            ) % futurePrime
            if residues[futureIndex] == 0:
                dividesSomeA[futureIndex] = True

    return sum(prime for prime, divides in zip(primes, dividesSomeA) if divides)


def runTests():
    assert chineseLeftoverA(2) == 5
    assert chineseLeftoverA(3) == 23
    assert chineseLeftoverA(4) == 53
    assert chineseLeftoverA(5) == 1_523
    assert primeDivisorSum(50) == 69


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeDivisorSum(300_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
