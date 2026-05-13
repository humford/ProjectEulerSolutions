import time


MODULUS = 1_000_000_000


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)
    return [number for number, is_prime in enumerate(sieve) if is_prime]


def primeFactorSumValues(limit):
    values = [0] * (limit + 1)
    values[0] = 1
    for prime in primesUpTo(limit):
        for total in range(prime, limit + 1):
            values[total] = (values[total] + prime * values[total - prime]) % MODULUS
    values[0] = 0
    return values


def fibonacciNumbers(count):
    fibs = [0, 1, 1]
    while len(fibs) <= count:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def fibonacciPrimeFactorSum(first, last):
    fibs = fibonacciNumbers(last)
    values = primeFactorSumValues(fibs[last])
    return sum(values[fibs[index]] for index in range(first, last + 1)) % MODULUS


def runTests():
    values = primeFactorSumValues(8)
    assert values[1] == 0
    assert values[2] == 2
    assert values[3] == 3
    assert values[5] == 11
    assert values[8] == 49


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciPrimeFactorSum(2, 24)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
