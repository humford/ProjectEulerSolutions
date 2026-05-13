import time


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)
    return [number for number, is_prime in enumerate(sieve) if is_prime]


def asymptoticSquarePrimeFactorCoefficient(k, prime_limit=1_000_000):
    probabilities = [0.0] * (k + 1)
    probabilities[0] = 1.0
    for prime in primesUpTo(prime_limit):
        square_probability = 1.0 / (prime * prime)
        for index in range(k, 0, -1):
            probabilities[index] = probabilities[index] * (1.0 - square_probability) + probabilities[index - 1] * square_probability
        probabilities[0] *= 1.0 - square_probability
    return probabilities[k]


def formattedCoefficient(k):
    return f"{asymptoticSquarePrimeFactorCoefficient(k):.4e}"


def runTests():
    assert f"{asymptoticSquarePrimeFactorCoefficient(0):.5f}" == "0.60793"
    assert formattedCoefficient(7) == "1.0012e-10"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formattedCoefficient(7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
