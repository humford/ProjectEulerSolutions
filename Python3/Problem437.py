import time


def primeList(limit):
    isPrime = bytearray(b"\x01") * limit
    isPrime[:2] = b"\x00\x00"

    for number in range(2, int(limit**0.5) + 1):
        if isPrime[number]:
            start = number * number
            isPrime[start:limit:number] = b"\x00" * (
                ((limit - 1 - start) // number) + 1
            )

    return [number for number in range(limit) if isPrime[number]]


def distinctPrimeFactors(number, factorPrimes):
    factors = []

    for prime in factorPrimes:
        if prime * prime > number:
            break

        if number % prime == 0:
            factors.append(prime)

            while number % prime == 0:
                number //= prime

    if number > 1:
        factors.append(number)

    return factors


def fibonacciPair(index, modulus):
    current = 0
    nextValue = 1

    for bit in bin(index)[2:]:
        doubled = current * ((2 * nextValue - current) % modulus) % modulus
        advanced = (current * current + nextValue * nextValue) % modulus

        if bit == "0":
            current, nextValue = doubled, advanced
        else:
            current, nextValue = advanced, (doubled + advanced) % modulus

    return current, nextValue


def hasFibonacciPrimitiveRoot(prime, factorPrimes):
    if prime == 5:
        return True
    if prime % 5 not in (1, 4):
        return False

    period = prime - 1
    return all(
        fibonacciPair(period // factor, prime) != (0, 1)
        for factor in distinctPrimeFactors(period, factorPrimes)
    )


def fibonacciPrimitiveRootStats(limit):
    primes = primeList(limit)
    factorPrimes = [prime for prime in primes if prime * prime < limit]
    selected = [
        prime
        for prime in primes
        if hasFibonacciPrimitiveRoot(prime, factorPrimes)
    ]
    return len(selected), sum(selected)


def primeSum(limit=100_000_000):
    return fibonacciPrimitiveRootStats(limit)[1]


def runTests():
    assert fibonacciPair(10, 11) == (0, 1)
    assert hasFibonacciPrimitiveRoot(11, [2, 3]) is True
    assert fibonacciPrimitiveRootStats(10_000) == (323, 1480491)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
