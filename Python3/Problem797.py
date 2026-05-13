import time
from array import array


MOD = 1_000_000_007


def linearSieveMobiusSmallestPrimeFactor(limit):
    mobius = array("b", [0]) * (limit + 1)
    smallestPrimeFactor = array("I", [0]) * (limit + 1)
    primes = []
    mobius[1] = 1
    smallestPrimeFactor[1] = 1

    for n in range(2, limit + 1):
        if smallestPrimeFactor[n] == 0:
            smallestPrimeFactor[n] = n
            primes.append(n)
            mobius[n] = -1

        for prime in primes:
            value = n * prime
            if value > limit:
                break
            smallestPrimeFactor[value] = prime
            if n % prime == 0:
                mobius[value] = 0
                break
            mobius[value] = -mobius[n]

    return mobius, smallestPrimeFactor


def buildTwoPowersMinusOneAndInverses(limit):
    values = array("I", [0]) * (limit + 1)
    inverses = array("I", [0]) * (limit + 1)

    power = 1
    for n in range(1, limit + 1):
        power = power * 2 % MOD
        values[n] = power - 1

    inverses[0] = 1
    product = 1
    for n in range(1, limit + 1):
        product = product * values[n] % MOD
        inverses[n] = product

    inverseProduct = pow(product, MOD - 2, MOD)
    for n in range(limit, 0, -1):
        previous = inverses[n - 1]
        inverses[n] = inverseProduct * previous % MOD
        inverseProduct = inverseProduct * values[n] % MOD

    inverses[0] = 0
    return values, inverses


def distinctPrimeFactors(n, smallestPrimeFactor):
    factors = []
    while n > 1:
        prime = smallestPrimeFactor[n]
        factors.append(prime)
        while n % prime == 0:
            n //= prime
    return factors


def cyclotomicValueAt2(n, smallestPrimeFactor, values, inverses):
    if n == 1:
        return 1

    products = [1]
    parity = [0]
    for prime in distinctPrimeFactors(n, smallestPrimeFactor):
        length = len(products)
        for i in range(length):
            products.append(products[i] * prime)
            parity.append(parity[i] ^ 1)

    result = 1
    for divisor, oddParity in zip(products, parity):
        index = n // divisor
        if oddParity:
            result = result * inverses[index] % MOD
        else:
            result = result * values[index] % MOD

    return result


def buildTPrefix(limit, smallestPrimeFactor, values, inverses):
    T = array("I", [1]) * (limit + 1)
    T[0] = 0

    for divisor in range(1, limit + 1):
        factor = cyclotomicValueAt2(divisor, smallestPrimeFactor, values, inverses) + 1
        if factor >= MOD:
            factor -= MOD
        for multiple in range(divisor, limit + 1, divisor):
            T[multiple] = T[multiple] * factor % MOD

    total = 0
    for n in range(1, limit + 1):
        total += T[n]
        if total >= MOD:
            total -= MOD
        T[n] = total

    return T


def divisorsSmall(n):
    divisors = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            divisors.append(d)
            if d * d != n:
                divisors.append(n // d)
        d += 1
    return divisors


def exampleChecks():
    limit = 10
    mobius, smallestPrimeFactor = linearSieveMobiusSmallestPrimeFactor(limit)
    values, inverses = buildTwoPowersMinusOneAndInverses(limit)
    T = array("I", [1]) * (limit + 1)
    T[0] = 0

    for divisor in range(1, limit + 1):
        factor = cyclotomicValueAt2(divisor, smallestPrimeFactor, values, inverses) + 1
        if factor >= MOD:
            factor -= MOD
        for multiple in range(divisor, limit + 1, divisor):
            T[multiple] = T[multiple] * factor % MOD

    def P(n):
        total = 0
        for divisor in divisorsSmall(n):
            total += mobius[divisor] * T[n // divisor]
        return total % MOD

    assert P(6) == 234
    assert sum(P(n) for n in range(1, 11)) % MOD == 5_598


def solve(limit):
    mobius, smallestPrimeFactor = linearSieveMobiusSmallestPrimeFactor(limit)
    values, inverses = buildTwoPowersMinusOneAndInverses(limit)
    TPrefix = buildTPrefix(limit, smallestPrimeFactor, values, inverses)
    del values, inverses, smallestPrimeFactor

    mobiusPrefix = array("i", [0]) * (limit + 1)
    total = 0
    for n in range(1, limit + 1):
        total += mobius[n]
        mobiusPrefix[n] = total

    answer = 0
    left = 1
    while left <= limit:
        quotient = limit // left
        right = limit // quotient
        mobiusSum = mobiusPrefix[right] - mobiusPrefix[left - 1]
        answer = (answer + (mobiusSum % MOD) * TPrefix[quotient]) % MOD
        left = right + 1

    return answer


def runTests():
    exampleChecks()


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve(10_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
