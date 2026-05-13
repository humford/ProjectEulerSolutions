from array import array
import math
import time


MODULUS = 1_000_000_993


def _is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True


def smoothPart(bound, n):
    result = 1
    for prime in range(2, bound + 1):
        if _is_prime(prime):
            while n % prime == 0:
                n //= prime
                result *= prime
    return result


def _sum_small(n):
    total = 0
    for bound in range(1, n + 1):
        for r in range(n + 1):
            total += smoothPart(bound, math.comb(n, r))
    return total


def buildSieveData(limit):
    leastPrime = array("I", [0]) * (limit + 1)
    primes = []

    for value in range(2, limit + 1):
        if leastPrime[value] == 0:
            leastPrime[value] = value
            primes.append(value)

        least = leastPrime[value]
        for prime in primes:
            composite = value * prime
            if composite > limit or prime > least:
                break
            leastPrime[composite] = prime

    primePosition = array("i", [-1]) * (limit + 1)
    inversePrime = array("I", [0]) * len(primes)
    weights = array("I", [0]) * len(primes)
    for index, prime in enumerate(primes):
        primePosition[prime] = index
        inversePrime[index] = pow(prime, MODULUS - 2, MODULUS)
        nextPrime = primes[index + 1] if index + 1 < len(primes) else limit + 1
        weights[index] = nextPrime - prime

    stripNext = array("I", [1]) * (limit + 1)
    stripPosition = array("I", [0]) * (limit + 1)
    stripMultiply = array("I", [1]) * (limit + 1)
    stripDivide = array("I", [1]) * (limit + 1)

    for value in range(2, limit + 1):
        prime = leastPrime[value]
        reduced = value // prime
        position = primePosition[prime]
        stripPosition[value] = position

        if reduced > 1 and leastPrime[reduced] == prime:
            stripNext[value] = stripNext[reduced]
            stripMultiply[value] = stripMultiply[reduced] * prime % MODULUS
            stripDivide[value] = stripDivide[reduced] * inversePrime[position] % MODULUS
        else:
            stripNext[value] = reduced
            stripMultiply[value] = prime
            stripDivide[value] = inversePrime[position]

    return weights, stripNext, stripPosition, stripMultiply, stripDivide


class PrefixProductTree:
    def __init__(self, weights):
        size = 1
        while size < len(weights):
            size *= 2
        self.size = size
        self.product = array("I", [1]) * (2 * size)
        self.total = array("I", [0]) * (2 * size)

        for index, weight in enumerate(weights):
            self.total[size + index] = weight
        for node in range(size - 1, 0, -1):
            self._pull(node)

    def _pull(self, node):
        left = 2 * node
        right = left + 1
        self.product[node] = self.product[left] * self.product[right] % MODULUS
        self.total[node] = (self.total[left] + self.product[left] * self.total[right]) % MODULUS

    def multiplyPrimePower(self, primePosition, factor):
        node = self.size + primePosition
        self.product[node] = self.product[node] * factor % MODULUS
        self.total[node] = self.total[node] * factor % MODULUS

        node //= 2
        while node:
            self._pull(node)
            node //= 2

    def rowContribution(self):
        return (self.total[1] + 1) % MODULUS


def applyFactor(value, factors, positions, stripNext, stripPosition, stripFactor):
    while value > 1:
        position = stripPosition[value]
        factor = stripFactor[value]
        for index, existing in enumerate(positions):
            if existing == position:
                factors[index] = factors[index] * factor % MODULUS
                break
        else:
            positions.append(position)
            factors.append(factor)
        value = stripNext[value]


def smoothBinomialSum(n):
    weights, stripNext, stripPosition, stripMultiply, stripDivide = buildSieveData(n)
    tree = PrefixProductTree(weights)
    total = 0
    half = n // 2

    for r in range(half + 1):
        contribution = tree.rowContribution()
        total += contribution if r == n - r else 2 * contribution
        total %= MODULUS

        if r == half:
            break

        positions = []
        factors = []
        applyFactor(n - r, factors, positions, stripNext, stripPosition, stripMultiply)
        applyFactor(r + 1, factors, positions, stripNext, stripPosition, stripDivide)
        for position, factor in zip(positions, factors):
            if factor != 1:
                tree.multiplyPrimePower(position, factor)

    return total


def runTests():
    assert smoothPart(1, 10) == 1
    assert smoothPart(4, 2100) == 12
    assert smoothPart(17, 2_496_144) == 5712
    assert _sum_small(11) == 3132
    assert smoothBinomialSum(1_111) == 706_036_312
    assert smoothBinomialSum(111_111) == 22_156_169


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = smoothBinomialSum(11_111_111)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
