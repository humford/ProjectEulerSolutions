import time
from array import array


def divisorCounts(limit):
    smallest_prime_factor = array("I", [0]) * (limit + 1)
    prime_exponent = array("B", [0]) * (limit + 1)
    divisors = array("H", [0]) * (limit + 1)
    primes = []
    divisors[1] = 1

    for number in range(2, limit + 1):
        if smallest_prime_factor[number] == 0:
            smallest_prime_factor[number] = number
            prime_exponent[number] = 1
            divisors[number] = 2
            primes.append(number)

        for prime in primes:
            multiple = number * prime
            if multiple > limit:
                break

            smallest_prime_factor[multiple] = prime
            if prime == smallest_prime_factor[number]:
                next_exponent = prime_exponent[number] + 1
                prime_exponent[multiple] = next_exponent
                divisors[multiple] = (
                    divisors[number] // (prime_exponent[number] + 1) * (next_exponent + 1)
                )
                break

            prime_exponent[multiple] = 1
            divisors[multiple] = divisors[number] * 2

    return divisors


def consecutiveDivisorPairs(limit):
    divisors = divisorCounts(limit)
    return sum(1 for number in range(2, limit) if divisors[number] == divisors[number + 1])


def runTests():
    assert consecutiveDivisorPairs(10) == 1


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = consecutiveDivisorPairs(10000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
