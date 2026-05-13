from array import array
from math import gcd, isqrt
import time


TARGET_N = 123_567_101_113
SPLIT_D = 100_000_000


def tonelliMinusOne(p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    m = s
    c = pow(z, q, p)
    t = pow(p - 1, q, p)
    r = pow(p - 1, (q + 1) // 2, p)

    while t != 1:
        i = 1
        tt = t * t % p
        while tt != 1:
            tt = tt * tt % p
            i += 1

        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p

    return r


def sqrtMinusOnePrimeSquare(p):
    root = tonelliMinusOne(p)
    correction = -((root * root + 1) // p) * pow(2 * root, -1, p)
    lifted = root + (correction % p) * p
    return lifted % (p * p)


def primesOneModFourWithRoots(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, isqrt(limit) + 1):
        if isPrime[n]:
            start = n * n
            isPrime[start:limit + 1:n] = b"\x00" * (((limit - start) // n) + 1)

    primes = array("I")
    roots = array("Q")

    for prime in range(5, limit + 1, 4):
        if isPrime[prime]:
            root = sqrtMinusOnePrimeSquare(prime)
            primes.append(prime)
            roots.append(root)

    return primes, roots


def countRootsUpTo(limit, modulus, roots):
    quotient = limit // modulus
    remainder = limit % modulus
    total = 0

    for root in roots:
        total += quotient
        if root <= remainder:
            total += 1

    return total


def smallDivisorContribution(limit, split):
    primes, primeRoots = primesOneModFourWithRoots(split)
    primeCount = len(primes)
    total = 0

    def search(start, divisor, roots, oddPrimeCount):
        nonlocal total

        divisorSquare = divisor * divisor

        for i in range(start, primeCount):
            prime = primes[i]
            newDivisor = divisor * prime
            if newDivisor > split:
                break

            primeSquare = prime * prime
            root = primeRoots[i]
            otherRoot = primeSquare - root

            if divisor == 1:
                newRoots = [root, otherRoot]
            else:
                inverse = pow(divisorSquare % primeSquare, -1, primeSquare)
                newRoots = []

                for oldRoot in roots:
                    offset = (root - oldRoot) % primeSquare
                    newRoots.append(oldRoot + divisorSquare * (offset * inverse % primeSquare))

                    offset = (otherRoot - oldRoot) % primeSquare
                    newRoots.append(oldRoot + divisorSquare * (offset * inverse % primeSquare))

            newModulus = newDivisor * newDivisor
            count = countRootsUpTo(limit, newModulus, newRoots)

            if oddPrimeCount:
                total -= count
            else:
                total += count

            search(i + 1, newDivisor, newRoots, not oddPrimeCount)

    search(0, 1, [0], False)
    return total


def squarefreeTable(limit):
    squarefree = bytearray(b"\x01") * (limit + 1)
    squarefree[0] = 0

    for n in range(2, isqrt(limit) + 1):
        square = n * n
        for multiple in range(square, limit + 1, square):
            squarefree[multiple] = 0

    return squarefree


def negativePellFundamental(d):
    root = isqrt(d)
    if root * root == d:
        return None

    m = 0
    denominator = 1
    a = root
    period = 0

    pPrevPrev, pPrev = 0, 1
    qPrevPrev, qPrev = 1, 0

    while True:
        p = a * pPrev + pPrevPrev
        q = a * qPrev + qPrevPrev

        if p * p - d * q * q == -1:
            return p, q

        pPrevPrev, pPrev = pPrev, p
        qPrevPrev, qPrev = qPrev, q

        m = denominator * a - m
        denominator = (d - m * m) // denominator
        a = (root + m) // denominator
        period += 1

        if a == 2 * root and period % 2 == 0:
            return None


def smallPrimes(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, isqrt(limit) + 1):
        if isPrime[n]:
            start = n * n
            isPrime[start:limit + 1:n] = b"\x00" * (((limit - start) // n) + 1)

    return [n for n in range(2, limit + 1) if isPrime[n]]


def distinctPrimeFactors(n, primes):
    factors = []

    for prime in primes:
        if prime * prime > n:
            break

        if n % prime == 0:
            factors.append(prime)
            while n % prime == 0:
                n //= prime

    if n > 1:
        factors.append(n)

    return factors


def largeDivisorSubsetContribution(factors, split):
    total = 0

    def search(index, product, oddPrimeCount):
        nonlocal total

        if index == len(factors):
            if product > split:
                total += 1 if oddPrimeCount else -1
            return

        search(index + 1, product, oddPrimeCount)
        search(index + 1, product * factors[index], not oddPrimeCount)

    search(0, 1, False)
    return total


def largeDivisorContribution(limit, split):
    maxK = (limit * limit + 1) // ((split + 1) * (split + 1))
    if maxK < 2:
        return 0

    squarefree = squarefreeTable(maxK)
    factorPrimes = smallPrimes(isqrt(limit) + 1)
    total = 0

    for k in range(2, maxK + 1):
        if not squarefree[k]:
            continue

        solution = negativePellFundamental(k)
        if solution is None:
            continue

        x, y = solution
        multiplierX = x * x + k * y * y
        multiplierY = 2 * x * y

        while x <= limit:
            if y > split:
                factors = distinctPrimeFactors(y, factorPrimes)
                total += largeDivisorSubsetContribution(factors, split)

            x, y = (
                multiplierX * x + multiplierY * k * y,
                multiplierX * y + multiplierY * x,
            )

    return total


def C(limit, split=SPLIT_D):
    split = min(split, limit)
    nonSquarefree = (
        smallDivisorContribution(limit, split)
        + largeDivisorContribution(limit, split)
    )
    return limit - nonSquarefree


def bruteC(limit):
    count = 0

    for x in range(1, limit + 1):
        value = x * x + 1
        squarefree = True
        prime = 2
        while prime * prime <= value:
            square = prime * prime
            if value % square == 0:
                squarefree = False
                break
            prime += 1
        if squarefree:
            count += 1

    return count


def runTests():
    assert bruteC(10) == 9
    assert C(10, 10) == 9
    assert C(1000, 1000) == 895


def solve():
    return C(TARGET_N)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
