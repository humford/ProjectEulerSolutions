import time
from array import array


MODULUS = 10**9
PROBLEM_LIMIT = 10**11
SIEVE_LIMIT = 5_000_000


def divisorSum(number):
    return sum(divisor for divisor in range(1, number + 1) if number % divisor == 0)


def bruteS(limit):
    return sum(
        divisorSum(i * j)
        for i in range(1, limit + 1)
        for j in range(1, limit + 1)
    )


def sumIntegers(first, last, modulus):
    return ((first + last) * (last - first + 1) // 2) % modulus


class DivisorProductSummer:
    # sigma(i*j) = sum d*mu(d)*sigma(i/d)*sigma(j/d) over d | gcd(i, j).
    # This turns the double sum into blocks of weighted Mobius prefixes.
    def __init__(self, sieveLimit=SIEVE_LIMIT, modulus=MODULUS):
        self.sieveLimit = sieveLimit
        self.modulus = modulus
        self.weightedMobiusPrefix, self.divisorPrefix = self.buildPrefixes(sieveLimit)
        self.weightedMobiusCache = {}
        self.divisorSummatoryCache = {}

    def buildPrefixes(self, limit):
        mu = array("b", [0]) * (limit + 1)
        mu[1] = 1

        sigma = array("I", [0]) * (limit + 1)
        sigma[1] = 1

        primePower = array("I", [0]) * (limit + 1)
        primePower[1] = 1

        sigmaCore = array("I", [0]) * (limit + 1)
        sigmaCore[1] = 1

        isComposite = bytearray(limit + 1)
        primes = []

        for number in range(2, limit + 1):
            if not isComposite[number]:
                primes.append(number)
                mu[number] = -1
                primePower[number] = number
                sigmaCore[number] = 1
                sigma[number] = 1 + number

            for prime in primes:
                composite = number * prime
                if composite > limit:
                    break

                isComposite[composite] = 1

                if number % prime == 0:
                    mu[composite] = 0
                    nextPower = primePower[number] * prime
                    primePower[composite] = nextPower
                    sigmaCore[composite] = sigmaCore[number]
                    sigma[composite] = (
                        sigmaCore[composite] * ((nextPower * prime - 1) // (prime - 1))
                    )
                    break

                mu[composite] = -mu[number]
                primePower[composite] = prime
                sigmaCore[composite] = sigma[number]
                sigma[composite] = sigma[number] * (1 + prime)

        weightedMobiusPrefix = array("I", [0]) * (limit + 1)
        divisorPrefix = array("I", [0]) * (limit + 1)

        weightedMobiusTotal = 0
        divisorTotal = 0

        for number in range(1, limit + 1):
            weightedMobiusTotal = (
                weightedMobiusTotal + number * mu[number]
            ) % self.modulus
            divisorTotal = (divisorTotal + sigma[number]) % self.modulus
            weightedMobiusPrefix[number] = weightedMobiusTotal
            divisorPrefix[number] = divisorTotal

        return weightedMobiusPrefix, divisorPrefix

    def weightedMobiusSummatory(self, limit):
        if limit <= self.sieveLimit:
            return self.weightedMobiusPrefix[limit]

        if limit in self.weightedMobiusCache:
            return self.weightedMobiusCache[limit]

        total = 1
        start = 2

        while start <= limit:
            quotient = limit // start
            end = limit // quotient
            if quotient <= self.sieveLimit:
                quotientSum = self.weightedMobiusPrefix[quotient]
            else:
                quotientSum = self.weightedMobiusSummatory(quotient)

            total = (
                total - sumIntegers(start, end, self.modulus) * quotientSum
            ) % self.modulus
            start = end + 1

        self.weightedMobiusCache[limit] = total
        return total

    def divisorSummatory(self, limit):
        if limit <= self.sieveLimit:
            return self.divisorPrefix[limit]

        if limit in self.divisorSummatoryCache:
            return self.divisorSummatoryCache[limit]

        total = 0
        start = 1

        while start <= limit:
            quotient = limit // start
            end = limit // quotient
            total = (
                total
                + (quotient % self.modulus) * sumIntegers(start, end, self.modulus)
            ) % self.modulus
            start = end + 1

        self.divisorSummatoryCache[limit] = total
        return total

    def S(self, limit):
        total = 0
        start = 1

        while start <= limit:
            quotient = limit // start
            end = limit // quotient
            mobiusBlock = (
                self.weightedMobiusSummatory(end)
                - self.weightedMobiusSummatory(start - 1)
            ) % self.modulus
            divisorTotal = self.divisorSummatory(quotient)

            total = (
                total + mobiusBlock * divisorTotal % self.modulus * divisorTotal
            ) % self.modulus
            start = end + 1

        return total


def runTests(summer):
    assert bruteS(3) == 59
    assert summer.S(3) == 59
    assert summer.S(10**3) == 563_576_517_282 % MODULUS
    assert summer.S(10**5) == 215_766_508


if __name__ == "__main__":
    startTime = time.time()
    summer = DivisorProductSummer()
    runTests(summer)
    answer = summer.S(PROBLEM_LIMIT)
    elapsed = time.time() - startTime

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
