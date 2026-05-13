import math
import time


LIMIT = 150


SEED = (1, 0)


def isPrime(number):
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2

    for divisor in range(3, math.isqrt(number) + 1, 2):
        if number % divisor == 0:
            return False

    return True


def squareSumPrimeRepresentation(prime):
    for a in range(1, math.isqrt(prime) + 1):
        b_squared = prime - a * a
        b = math.isqrt(b_squared)
        if b * b == b_squared:
            return min(a, b), max(a, b)

    raise ValueError("prime is not representable")


def combineRepresentations(first, second):
    a, b = first
    c, d = second
    result = []

    x = a * c + b * d
    y = abs(a * d - b * c)
    result.append((min(x, y), max(x, y)))

    if first != SEED:
        x = abs(a * c - b * d)
        y = a * d + b * c
        result.append((min(x, y), max(x, y)))

    return result


def sumOfSquareSumSolutions(limit):
    prime_representations = [
        squareSumPrimeRepresentation(number)
        for number in range(5, limit, 4)
        if isPrime(number)
    ]

    def search(index, representations):
        if index == len(prime_representations):
            return sum(a for a, b in representations if (a, b) != SEED)

        with_prime = []
        for representation in representations:
            with_prime.extend(
                combineRepresentations(representation, prime_representations[index])
            )

        return search(index + 1, representations) + search(index + 1, tuple(with_prime))

    return search(0, (SEED,))


def bruteSquareSumAValues(number):
    result = []

    for a in range(math.isqrt(number) + 1):
        b_squared = number - a * a
        b = math.isqrt(b_squared)
        if a <= b and b * b == b_squared:
            result.append(a)

    return result


def runTests():
    assert bruteSquareSumAValues(65) == [1, 4]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumOfSquareSumSolutions(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
