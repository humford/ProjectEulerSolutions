import math
import time


PROBLEM_LIMIT = 10**12


def bruteF(limit):
    count = 0

    for x in range(1, limit + 1):
        for y in range(x + 1, limit + 1):
            denominator = x + y

            if x * y % denominator == 0:
                count += 1

    return count


def mobiusSieve(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1

    isComposite = bytearray(limit + 1)
    primes = []

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            mu[number] = -1

        for prime in primes:
            composite = number * prime
            if composite > limit:
                break

            isComposite[composite] = 1
            if number % prime == 0:
                mu[composite] = 0
                break

            mu[composite] = -mu[number]

    return mu


def squareFreeDivisorsByNumber(limit, mu):
    divisors = [[] for _ in range(limit + 1)]

    for divisor in range(1, limit + 1):
        if mu[divisor]:
            for multiple in range(divisor, limit + 1, divisor):
                divisors[multiple].append((divisor, mu[divisor]))

    return divisors


def sumFloorRange(limit, first, last):
    if first > last or limit < first:
        return 0

    last = min(last, limit)
    total = 0

    while first <= last:
        quotient = limit // first
        end = min(last, limit // quotient)
        total += quotient * (end - first + 1)
        first = end + 1

    return total


def maxV(limit):
    value = (math.isqrt(1 + 4 * limit) - 1) // 2

    while value * (value + 1) > limit:
        value -= 1
    while (value + 1) * (value + 2) <= limit:
        value += 1

    return value


def reciprocalSolutionCount(limit):
    vLimit = maxV(limit)
    mu = mobiusSieve(vLimit)
    divisors = squareFreeDivisorsByNumber(vLimit, mu)
    total = 0

    # With gcd(u,v)=1 and u<v, all solutions are
    # x=t*u*(u+v), y=t*v*(u+v), n=t*u*v.
    # Thus y<=L contributes floor(L/(v*(u+v))) for each coprime pair.
    for v in range(2, vLimit + 1):
        quotient = limit // v
        maxW = min(2 * v - 1, quotient)

        for divisor, muValue in divisors[v]:
            first = v // divisor + 1
            last = maxW // divisor
            total += muValue * sumFloorRange(quotient // divisor, first, last)

    return total


def runTests():
    assert bruteF(15) == 4
    assert reciprocalSolutionCount(15) == 4
    assert reciprocalSolutionCount(1000) == 1069


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = reciprocalSolutionCount(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
