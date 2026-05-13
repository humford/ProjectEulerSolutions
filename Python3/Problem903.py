from array import array
from itertools import permutations
import time


MODULUS = 1_000_000_007
TARGET_N = 1_000_000


def rankSmall(permutation):
    n = len(permutation)
    available = list(range(1, n + 1))
    factorials = [1] * (n + 1)
    for index in range(2, n + 1):
        factorials[index] = index * factorials[index - 1]

    rank = 1
    for index, value in enumerate(permutation):
        position = available.index(value)
        rank += position * factorials[n - index - 1]
        available.pop(position)

    return rank


def compose(permutation, current):
    return tuple(permutation[current[index] - 1] for index in range(len(permutation)))


def bruteQ(n):
    factorial = 1
    for index in range(2, n + 1):
        factorial *= index

    total = 0
    identity = tuple(range(1, n + 1))
    for permutation in permutations(identity):
        current = identity
        for _ in range(factorial):
            current = compose(permutation, current)
            total += rankSmall(current)

    return total


def mobiusSieve(limit):
    mobius = array("b", [0]) * (limit + 1)
    mobius[1] = 1
    primes = []
    composite = bytearray(limit + 1)

    for value in range(2, limit + 1):
        if not composite[value]:
            primes.append(value)
            mobius[value] = -1
        for prime in primes:
            multiple = value * prime
            if multiple > limit:
                break
            composite[multiple] = 1
            if value % prime == 0:
                mobius[multiple] = 0
                break
            mobius[multiple] = -mobius[value]

    return mobius


def computeQ(n):
    if n <= 7:
        return bruteQ(n) % MODULUS

    inverses = array("I", [0]) * (n + 1)
    inverses[1] = 1
    for value in range(2, n + 1):
        inverses[value] = MODULUS - (MODULUS // value) * inverses[MODULUS % value] % MODULUS

    harmonic = array("I", [0]) * (n + 1)
    total = 0
    for value in range(1, n + 1):
        total += inverses[value]
        if total >= MODULUS:
            total -= MODULUS
        harmonic[value] = total

    mobius = mobiusSieve(n)
    convolution = array("I", [0]) * (n + 1)

    for divisor in range(1, n + 1):
        mu = mobius[divisor]
        if mu == 0:
            continue
        coefficient = inverses[divisor] if mu == 1 else MODULUS - inverses[divisor]
        quotient = 1
        for multiple in range(divisor, n + 1, divisor):
            convolution[multiple] = (
                convolution[multiple]
                + coefficient * harmonic[quotient - 1]
            ) % MODULUS
            quotient += 1

    correction = 0
    for cycleLength in range(2, n + 1):
        term = harmonic[n // cycleLength]
        term = term * (2 * convolution[cycleLength] % MODULUS) % MODULUS
        term = term * inverses[cycleLength] % MODULUS
        correction = (correction + term) % MODULUS

    alphaNumerator = (n - harmonic[n] + correction) % MODULUS
    alpha = alphaNumerator * inverses[n] % MODULUS * inverses[n - 1] % MODULUS

    beta = (
        harmonic[n // 2]
        * pow(2 * n * (n - 1) % MODULUS, MODULUS - 2, MODULUS)
    ) % MODULUS

    fixedProbability = harmonic[n] * inverses[n] % MODULUS
    otherProbability = (1 - fixedProbability) % MODULUS * inverses[n - 1] % MODULUS

    a = (fixedProbability - alpha) % MODULUS * inverses[n - 2] % MODULUS
    b = (otherProbability - beta) % MODULUS * inverses[n - 2] % MODULUS
    eta = (otherProbability - a - b) % MODULUS * inverses[n - 3] % MODULUS

    bulk = (n - 2) * (n - 3) // 2 % MODULUS
    constant = (
        beta
        + (n - 3) * b
        + (n - 1) * a
        + eta * bulk
    ) % MODULUS
    slope = (b - a) % MODULUS
    inverseTwo = (MODULUS + 1) // 2

    factorial = 1
    weighted1 = 0
    weighted2 = 0
    for m in range(1, n):
        factorial = factorial * m % MODULUS
        weighted1 = (weighted1 + factorial * m) % MODULUS
        weighted2 = (
            weighted2
            + factorial * m % MODULUS * (m + 1) % MODULUS * inverseTwo
        ) % MODULUS

    factorialN = factorial * n % MODULUS
    expectedRank = (1 + constant * weighted1 + slope * weighted2) % MODULUS
    return factorialN * factorialN % MODULUS * expectedRank % MODULUS


def solve():
    return computeQ(TARGET_N)


def runTests():
    assert computeQ(2) == 5
    assert computeQ(3) == 88
    assert computeQ(6) == 133103808
    assert computeQ(10) == 468421536
    assert solve() == 128553191


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
