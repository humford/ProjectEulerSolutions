import time


TARGET = 100_000_000


class PrimeRuns:
    def __init__(self):
        self.primes = []
        self.candidate = 2
        self.first = True
        self.onesRemaining = 0
        self.emitTwo = False

    def nextPrime(self):
        while True:
            candidate = self.candidate
            self.candidate += 1 if candidate == 2 else 2

            isPrime = True
            for prime in self.primes:
                if prime * prime > candidate:
                    break
                if candidate % prime == 0:
                    isPrime = False
                    break

            if isPrime:
                self.primes.append(candidate)
                return candidate

    def next(self):
        if self.first:
            self.first = False
            return 2

        if self.onesRemaining:
            self.onesRemaining -= 1
            return 1

        if self.emitTwo:
            self.emitTwo = False
            return 2

        prime = self.nextPrime()
        self.onesRemaining = prime - 1
        self.emitTwo = True
        return 1


def betaCoefficients(count):
    alpha = PrimeRuns()
    a, b, c, d = 2, 3, 3, 2
    coefficients = []

    while len(coefficients) < count:
        if c and d and a // c == b // d:
            coefficient = a // c
            coefficients.append(coefficient)
            a, b, c, d = c, d, a - coefficient * c, b - coefficient * d
        else:
            coefficient = alpha.next()
            a, b = a * coefficient + b, a
            c, d = c * coefficient + d, c

    return coefficients


def coefficientSum(count):
    alpha = PrimeRuns()
    a, b, c, d = 2, 3, 3, 2
    produced = 0
    total = 0

    while produced < count:
        if c and d and a // c == b // d:
            coefficient = a // c
            total += coefficient
            produced += 1
            a, b, c, d = c, d, a - coefficient * c, b - coefficient * d
        else:
            coefficient = alpha.next()
            a, b = a * coefficient + b, a
            c, d = c * coefficient + d, c

    return total


def solve():
    return coefficientSum(TARGET)


def runTests():
    firstTen = [0, 1, 5, 6, 16, 9, 1, 10, 16, 11]
    assert betaCoefficients(10) == firstTen
    assert coefficientSum(10) == 75


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
