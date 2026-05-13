from array import array
import time


MODULUS = 1_000_000_007
PREFIX_LIMIT = 10_000_000


def totientPrefix(limit):
    phi = array("Q", [0]) * (limit + 1)
    isComposite = bytearray(limit + 1)
    primes = []
    if limit >= 1:
        phi[1] = 1

    for n in range(2, limit + 1):
        if not isComposite[n]:
            primes.append(n)
            phi[n] = n - 1
        for prime in primes:
            value = n * prime
            if value > limit:
                break
            isComposite[value] = 1
            if n % prime == 0:
                phi[value] = phi[n] * prime
                break
            phi[value] = phi[n] * (prime - 1)

    total = 0
    for n in range(1, limit + 1):
        total += phi[n]
        phi[n] = total
    return phi


class TotientSum:
    def __init__(self, limit):
        self.prefix = totientPrefix(min(limit, PREFIX_LIMIT))
        self.cache = {}

    def sumTo(self, limit):
        if limit < len(self.prefix):
            return self.prefix[limit]
        if limit in self.cache:
            return self.cache[limit]

        total = limit * (limit + 1) // 2
        start = 2
        while start <= limit:
            quotient = limit // start
            end = limit // quotient
            total -= (end - start + 1) * self.sumTo(quotient)
            start = end + 1

        self.cache[limit] = total
        return total


def polarPolygonCount(limit, modulus=MODULUS):
    totients = TotientSum(limit)
    directionProduct = 1
    directionWeightSum = 0
    directionSquareWeightSum = 0

    start = 1
    while start <= limit:
        quotient = limit // start
        end = limit // quotient
        primitivePairs = 4 * (totients.sumTo(end) - totients.sumTo(start - 1))
        weight = quotient % modulus

        base = (quotient + 1) % modulus
        if base == 0:
            directionProduct = 0
        else:
            directionProduct *= pow(base, primitivePairs % (modulus - 1), modulus)
            directionProduct %= modulus

        directionWeightSum += primitivePairs * weight
        directionWeightSum %= modulus
        directionSquareWeightSum += primitivePairs * weight * weight
        directionSquareWeightSum %= modulus
        start = end + 1

    return (
        directionProduct * directionProduct
        - 2 * directionProduct * directionWeightSum
        + directionSquareWeightSum
        - 1
    ) % modulus


def polarPolygonCountSmall(limit):
    totients = TotientSum(limit)
    directionProduct = 1
    directionWeightSum = 0
    directionSquareWeightSum = 0

    for denominator in range(1, limit + 1):
        primitivePairs = 4 * (totients.sumTo(denominator) - totients.sumTo(denominator - 1))
        weight = limit // denominator
        directionProduct *= (weight + 1) ** primitivePairs
        directionWeightSum += primitivePairs * weight
        directionSquareWeightSum += primitivePairs * weight * weight

    return (
        directionProduct * directionProduct
        - 2 * directionProduct * directionWeightSum
        + directionSquareWeightSum
        - 1
    )


def runTests():
    assert polarPolygonCountSmall(1) == 131
    assert polarPolygonCountSmall(2) == 1_648_531
    assert polarPolygonCountSmall(3) == 1_099_461_296_175
    assert polarPolygonCount(343) == 937_293_740


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = polarPolygonCount(7 ** 13)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
