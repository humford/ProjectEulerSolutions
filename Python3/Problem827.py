import decimal
import functools
import math
import random
import sys
import time


MOD = 409_120_391
decimal.getcontext().prec = 90
LN2 = decimal.Decimal(2).ln()


def log2Int(n):
    return decimal.Decimal(n).ln() / LN2


def isPrime(n):
    if n < 2:
        return False

    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % prime == 0:
            return n == prime

    d = n - 1
    shifts = 0
    while d % 2 == 0:
        d //= 2
        shifts += 1

    for witness in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if witness % n == 0:
            continue
        x = pow(witness, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(shifts - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True


def pollardRho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    if n % 5 == 0:
        return 5

    while True:
        c = random.randrange(1, n - 1)
        x = random.randrange(0, n - 1)
        y = x
        divisor = 1

        while divisor == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            divisor = math.gcd(abs(x - y), n)

        if divisor != n:
            return divisor


FACTOR_CACHE = {}


def factor(n):
    if n in FACTOR_CACHE:
        return dict(FACTOR_CACHE[n])

    result = {}

    def recurse(m):
        if m == 1:
            return
        if isPrime(m):
            result[m] = result.get(m, 0) + 1
            return
        divisor = pollardRho(m)
        recurse(divisor)
        recurse(m // divisor)

    recurse(n)
    FACTOR_CACHE[n] = result
    return dict(result)


def divisorsFromFactors(factors):
    divisors = [1]
    for prime, exponent in factors.items():
        nextDivisors = []
        power = 1
        for _ in range(exponent + 1):
            for divisor in divisors:
                nextDivisors.append(divisor * power)
            power *= prime
        divisors = nextDivisors
    return divisors


ODD_DIVISORS_CACHE = {}


def oddDivisors(n):
    if n not in ODD_DIVISORS_CACHE:
        divisors = [d for d in divisorsFromFactors(factor(n)) if d % 2 == 1]
        divisors.sort()
        ODD_DIVISORS_CACHE[n] = divisors
    return ODD_DIVISORS_CACHE[n]


def primesByMod4(target, count):
    primes = []
    candidate = 2

    while len(primes) < count:
        if candidate % 4 == target:
            isCandidatePrime = True
            if candidate < 2:
                isCandidatePrime = False
            elif candidate % 2 == 0:
                isCandidatePrime = candidate == 2
            else:
                divisor = 3
                while divisor * divisor <= candidate:
                    if candidate % divisor == 0:
                        isCandidatePrime = False
                        break
                    divisor += 2
            if isCandidatePrime:
                primes.append(candidate)
        candidate += 1

    return primes


PRIMES_1_MOD4 = primesByMod4(1, 80)
PRIMES_3_MOD4 = primesByMod4(3, 80)
LOGS_1_MOD4 = [log2Int(p) for p in PRIMES_1_MOD4]
LOGS_3_MOD4 = [log2Int(p) for p in PRIMES_3_MOD4]
LOG2_2 = log2Int(2)


MIN_REP_CACHE = {}


def minRepForProduct(product, primes, logs):
    if product == 1:
        return decimal.Decimal(0), ()

    key = (product, primes[0])
    if key in MIN_REP_CACHE:
        return MIN_REP_CACHE[key]

    @functools.lru_cache(maxsize=None)
    def dfs(remaining, index, previousFactor):
        if remaining == 1:
            return decimal.Decimal(0), ()
        if index >= len(primes):
            return None

        best = None
        bestLog = None
        for factorValue in reversed(oddDivisors(remaining)):
            if factorValue == 1 or factorValue > previousFactor:
                continue
            exponent = (factorValue - 1) // 2
            if exponent <= 0:
                continue

            sub = dfs(remaining // factorValue, index + 1, factorValue)
            if sub is None:
                continue

            subLog, subExponents = sub
            currentLog = logs[index] * exponent + subLog
            if best is None or currentLog < bestLog:
                bestLog = currentLog
                best = currentLog, (exponent,) + subExponents

        return best

    result = dfs(product, 0, product)
    if result is None:
        raise RuntimeError("No representation found")
    MIN_REP_CACHE[key] = result
    return result


def repMod(rep, primes, modulus):
    _, exponents = rep
    result = 1
    for prime, exponent in zip(primes, exponents):
        result = result * pow(prime, exponent, modulus) % modulus
    return result


def repToInt(rep, primes):
    _, exponents = rep
    result = 1
    for prime, exponent in zip(primes, exponents):
        result *= prime ** exponent
    return result


BEST_D_CACHE = {}


def bestRepForD(D):
    if D == 1:
        return decimal.Decimal(0), 0, (decimal.Decimal(0), ())
    if D in BEST_D_CACHE:
        return BEST_D_CACHE[D]

    best = None
    bestLog = None

    for twoFactor in oddDivisors(D):
        if twoFactor == 1:
            e2 = 0
            logTwoPart = decimal.Decimal(0)
        else:
            e2 = (twoFactor + 1) // 2
            logTwoPart = LOG2_2 * e2

        rep3 = minRepForProduct(D // twoFactor, PRIMES_3_MOD4, LOGS_3_MOD4)
        currentLog = logTwoPart + rep3[0]
        if best is None or currentLog < bestLog:
            bestLog = currentLog
            best = currentLog, e2, rep3

    BEST_D_CACHE[D] = best
    return best


Q_CACHE = {}


def QRep(n):
    if n in Q_CACHE:
        return Q_CACHE[n]

    targetSum = n + 1
    best = None
    bestLog = None

    for B in oddDivisors(targetSum):
        rep1 = minRepForProduct(B, PRIMES_1_MOD4, LOGS_1_MOD4)
        D = (2 * targetSum) // B - 1
        logD, e2, rep3 = bestRepForD(D)
        currentLog = rep1[0] + logD
        if best is None or currentLog < bestLog:
            bestLog = currentLog
            best = currentLog, rep1, e2, rep3

    Q_CACHE[n] = best
    return best


def QMod(n, modulus=MOD):
    _, rep1, e2, rep3 = QRep(n)
    result = repMod(rep1, PRIMES_1_MOD4, modulus)
    result = result * pow(2, e2, modulus) % modulus
    result = result * repMod(rep3, PRIMES_3_MOD4, modulus) % modulus
    return result


def QExact(n):
    _, rep1, e2, rep3 = QRep(n)
    return repToInt(rep1, PRIMES_1_MOD4) * (1 << e2) * repToInt(rep3, PRIMES_3_MOD4)


def solve():
    total = 0
    for k in range(1, 19):
        total = (total + QMod(10 ** k)) % MOD
    return total


def runTests():
    assert QExact(5) == 15
    assert QExact(10) == 48
    assert QExact(10 ** 3) == 8_064_000


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    random.seed(0)
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
