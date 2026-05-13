import math
import time


LIMIT = 10**9


def isPrime(number):
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    if number % 3 == 0:
        return number == 3

    divisor = 5
    root = math.isqrt(number)

    while divisor <= root:
        if number % divisor == 0 or number % (divisor + 2) == 0:
            return False
        divisor += 6

    return True


def consecutivePrimes(limit):
    primes = []
    product = 1
    candidate = 2

    while product < limit:
        if isPrime(candidate):
            primes.append(candidate)
            product *= candidate
        candidate += 1

    return primes


def admissibleNumbers(limit):
    primes = consecutivePrimes(limit)
    result = set()

    def search(index, current):
        if current >= limit:
            return
        if index > 0:
            result.add(current)
        if index == len(primes):
            return

        value = current * primes[index]
        while value < limit:
            search(index + 1, value)
            value *= primes[index]

    search(0, 1)
    return result


def pseudoFortunateNumber(number):
    candidate = 3

    while not isPrime(number + candidate):
        candidate += 2

    return candidate


def pseudoFortunateSum(limit):
    return sum({pseudoFortunateNumber(number) for number in admissibleNumbers(limit)})


def runTests():
    assert sorted(admissibleNumbers(50)) == [2, 4, 6, 8, 12, 16, 18, 24, 30, 32, 36, 48]
    assert pseudoFortunateNumber(16) == 3
    assert pseudoFortunateNumber(630) == 11


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pseudoFortunateSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
