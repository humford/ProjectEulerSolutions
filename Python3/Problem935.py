import time


TARGET = 10**8


def mobiusPrefix(limit):
    mu = [0] * (limit + 1)
    prefix = [0] * (limit + 1)
    primes = []
    isComposite = [False] * (limit + 1)
    mu[1] = 1

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            mu[number] = -1

        for prime in primes:
            multiple = number * prime
            if multiple > limit:
                break

            isComposite[multiple] = True
            if number % prime == 0:
                mu[multiple] = 0
                break

            mu[multiple] = -mu[number]

    for number in range(1, limit + 1):
        prefix[number] = prefix[number - 1] + mu[number]

    return prefix


class Mertens:
    def __init__(self, limit):
        self.prefix = mobiusPrefix(limit)
        self.limit = limit
        self.mertensCache = {}
        self.oddCache = {}

    def total(self, n):
        if n <= self.limit:
            return self.prefix[n]
        if n in self.mertensCache:
            return self.mertensCache[n]

        value = 1
        index = 2
        while index <= n:
            quotient = n // index
            nextIndex = n // quotient
            value -= (nextIndex - index + 1) * self.total(quotient)
            index = nextIndex + 1

        self.mertensCache[n] = value
        return value

    def odd(self, n):
        if n <= 0:
            return 0
        if n in self.oddCache:
            return self.oddCache[n]

        value = 0
        current = n
        while current:
            value += self.total(current)
            current //= 2

        self.oddCache[n] = value
        return value

    def oddDelta(self, low, high):
        return self.odd(high) - self.odd(low - 1)

    def twoModFourDelta(self, low, high):
        return -self.odd(high // 2) + self.odd((low - 1) // 2)


def oddCountAndSum(limit):
    count = (limit + 1) // 2
    return count, count * count


def evenCountAndSum(limit):
    count = limit // 2
    return count, count * (count + 1)


def zeroModFourCountAndSum(limit):
    count = limit // 4
    return count, 2 * count * (count + 1)


def twoModFourCountAndSum(limit):
    count = (limit + 2) // 4
    return count, 2 * count * count


def classPairCount(maxT, residueClass, mertens):
    total = 0
    maxU = maxT - 1
    low = 1

    while low <= maxU:
        quotientForU = maxU // low
        quotientForT = maxT // low
        high = min(maxU // quotientForU, maxT // quotientForT)
        oddMu = mertens.oddDelta(low, high)
        twoModFourMu = mertens.twoModFourDelta(low, high)

        if residueClass == 1:
            count, valueSum = oddCountAndSum(quotientForU)
            total += oddMu * (quotientForT * count - valueSum)
        elif residueClass == 2:
            count, valueSum = twoModFourCountAndSum(quotientForU)
            total += oddMu * (quotientForT * count - valueSum)

            count, valueSum = oddCountAndSum(quotientForU)
            total += twoModFourMu * (quotientForT * count - valueSum)
        else:
            count, valueSum = zeroModFourCountAndSum(quotientForU)
            total += oddMu * (quotientForT * count - valueSum)

            count, valueSum = evenCountAndSum(quotientForU)
            total += twoModFourMu * (quotientForT * count - valueSum)

        low = high + 1

    return total


def F(maxSteps):
    limit = int(maxSteps ** (2 / 3)) + 100
    mertens = Mertens(limit)

    integerLengths = maxSteps // 4
    oddLimit = maxSteps // 4 + 1
    twoModFourLimit = maxSteps // 2 + 1
    zeroModFourLimit = maxSteps + 1

    nonIntegerOdd = classPairCount(oddLimit, 1, mertens) - (oddLimit - 1)
    nonIntegerTwoModFour = classPairCount(twoModFourLimit, 2, mertens)
    nonIntegerZeroModFour = classPairCount(zeroModFourLimit, 0, mertens)

    return (
        integerLengths
        + nonIntegerOdd
        + nonIntegerTwoModFour
        + nonIntegerZeroModFour
    )


def solve():
    return F(TARGET)


def runTests():
    assert F(6) == 4
    assert F(100) == 805


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
