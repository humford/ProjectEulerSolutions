import math
import time


MODULUS = 987_898_789
PROBLEM_LIMIT = 2_000


def tilings(length):
    if length == 0:
        return 1
    if length == 1:
        return 10

    previous, current = 1, 10

    for _ in range(2, length + 1):
        previous, current = current, 10 * current + previous

    return current


def bruteS(limit):
    cache = {}
    total = 0

    for c in range(1, limit + 1):
        for a in range(1, limit + 1):
            first = cache.setdefault(c**a, tilings(c**a))

            for b in range(1, limit + 1):
                total += math.gcd(first, cache.setdefault(c**b, tilings(c**b)))

    return total


def isPrime(number):
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2

    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2

    return True


def modularSquareRoot(number, prime):
    number %= prime
    if number == 0:
        return 0

    assert pow(number, (prime - 1) // 2, prime) == 1

    if prime % 4 == 3:
        return pow(number, (prime + 1) // 4, prime)

    oddPart = prime - 1
    twoPower = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        twoPower += 1

    nonResidue = 2
    while pow(nonResidue, (prime - 1) // 2, prime) != prime - 1:
        nonResidue += 1

    c = pow(nonResidue, oddPart, prime)
    x = pow(number, (oddPart + 1) // 2, prime)
    t = pow(number, oddPart, prime)
    m = twoPower

    while t != 1:
        i = 1
        tPower = pow(t, 2, prime)
        while tPower != 1:
            tPower = pow(tPower, 2, prime)
            i += 1

        b = pow(c, 1 << (m - i - 1), prime)
        c = pow(b, 2, prime)
        x = x * b % prime
        t = t * c % prime
        m = i

    return x


class LucasTiling:
    def __init__(self, modulus):
        assert isPrime(modulus)

        self.modulus = modulus
        self.period = modulus - 1
        self.sqrtDiscriminant = modularSquareRoot(104, modulus)
        self.inverseSqrtDiscriminant = pow(
            self.sqrtDiscriminant, modulus - 2, modulus
        )
        inverseTwo = pow(2, modulus - 2, modulus)
        self.alpha = (10 + self.sqrtDiscriminant) * inverseTwo % modulus
        self.beta = (10 - self.sqrtDiscriminant) * inverseTwo % modulus

        assert (self.alpha * self.alpha - 10 * self.alpha - 1) % modulus == 0
        assert (self.beta * self.beta - 10 * self.beta - 1) % modulus == 0

    def value(self, length):
        index = (length + 1) % self.period
        return (
            (pow(self.alpha, index, self.modulus) - pow(self.beta, index, self.modulus))
            * self.inverseSqrtDiscriminant
        ) % self.modulus


def specialPairCounts(limit):
    counts = [0] * (limit + 1)

    for a in range(1, limit + 1):
        aTwos = a & -a
        for b in range(1, limit + 1):
            if (b & -b) == aTwos:
                counts[math.gcd(a, b)] += 1

    return counts


def S(limit, modulus=MODULUS):
    lucas = LucasTiling(modulus)
    counts = specialPairCounts(limit)
    specialPairTotal = sum(counts)
    nonspecialPairs = limit * limit - specialPairTotal

    # T(n)=U(n+1) for U(0)=0, U(1)=1, U(k)=10U(k-1)+U(k-2).
    # gcd(U(m), U(n))=U(gcd(m,n)).  For c^a and c^b, the large gcd is
    # c^g+1 only when a/g and b/g are both odd; otherwise it is 1 or 2.
    total = nonspecialPairs * ((limit // 2) * 1 + ((limit + 1) // 2) * 10)
    total %= modulus

    for c in range(1, limit + 1):
        power = 1
        for exponentGcd in range(1, limit + 1):
            power = power * c % lucas.period
            count = counts[exponentGcd]
            if count:
                total = (total + count * lucas.value(power)) % modulus

    return total


def runTests():
    assert tilings(1) == 10
    assert tilings(2) == 101
    assert bruteS(2) == 10444
    assert bruteS(3) == 1_292_115_238_446_807_016_106_539_989
    assert S(2) == 10444
    assert S(3) == bruteS(3) % MODULUS
    assert S(4) == 670_616_280


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
