import math
import time


def smallestPrimeFactorSieve(limit):
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1

    root = math.isqrt(limit)
    for number in range(2, root + 1):
        if spf[number] == number:
            for multiple in range(number * number, limit + 1, number):
                if spf[multiple] == multiple:
                    spf[multiple] = number

    primes = [number for number in range(2, limit + 1) if spf[number] == number]
    return spf, primes


def multiplyQuadratic(left, right, modulus):
    a, b = left
    c, d = right
    return ((a * c + 7 * b * d) % modulus, (a * d + b * c) % modulus)


def quadraticPower(exponent, modulus):
    result = (1, 0)
    base = (1 % modulus, 1 % modulus)

    while exponent:
        if exponent % 2:
            result = multiplyQuadratic(result, base, modulus)
        base = multiplyQuadratic(base, base, modulus)
        exponent //= 2

    return result


def uniquePrimeFactors(number, spf):
    factors = []
    while number > 1:
        prime = spf[number]
        factors.append(prime)
        while number % prime == 0:
            number //= prime
    return factors


def primePowerOrders(limit, spf, primes):
    orders = [0] * (limit + 1)

    for prime in primes:
        if prime in (2, 3) or prime > limit:
            continue

        if prime == 7:
            order = 7
        else:
            residue = pow(7, (prime - 1) // 2, prime) == 1
            order = prime - 1 if residue else (prime - 1) * (prime + 1)
            factors = set(uniquePrimeFactors(prime - 1, spf))
            if not residue:
                factors.update(uniquePrimeFactors(prime + 1, spf))

            for factor in sorted(factors):
                while order % factor == 0 and quadraticPower(order // factor, prime) == (1, 0):
                    order //= factor

        primePower = prime
        currentOrder = order
        while primePower <= limit:
            orders[primePower] = currentOrder
            nextPrimePower = primePower * prime
            if nextPrimePower > limit:
                break
            if quadraticPower(currentOrder, nextPrimePower) != (1, 0):
                currentOrder *= prime
            primePower = nextPrimePower

    return orders


def powerOrder(x, spf, orders):
    if math.gcd(x, 6) != 1:
        return 0

    remaining = x
    result = 1
    while remaining > 1:
        prime = spf[remaining]
        primePower = 1
        while remaining % prime == 0:
            primePower *= prime
            remaining //= prime
        order = orders[primePower]
        result = result * order // math.gcd(result, order)

    return result


def powerOrderSum(limit):
    spf, primes = smallestPrimeFactorSieve(limit + 1)
    orders = primePowerOrders(limit, spf, primes)
    return sum(powerOrder(x, spf, orders) for x in range(2, limit + 1))


def runTests():
    spf, primes = smallestPrimeFactorSieve(1_001)
    orders = primePowerOrders(1_000, spf, primes)
    assert powerOrder(3, spf, orders) == 0
    assert powerOrder(5, spf, orders) == 12
    assert sum(powerOrder(x, spf, orders) for x in range(2, 101)) == 28_891
    assert sum(powerOrder(x, spf, orders) for x in range(2, 1_001)) == 13_131_583


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = powerOrderSum(10 ** 6)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
