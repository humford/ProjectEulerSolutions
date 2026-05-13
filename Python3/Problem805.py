import math
import time


MOD = 1_000_000_007


def primeSieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for n in range(2, math.isqrt(limit) + 1):
        if sieve[n]:
            start = n * n
            sieve[start: limit + 1: n] = b"\x00" * ((limit - start) // n + 1)

    return [n for n in range(limit + 1) if sieve[n]]


PRIMES = primeSieve(10_000)
ORDER_CACHE = {}


def factorize(n):
    factors = {}
    remaining = n

    for prime in PRIMES:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            factors[prime] = exponent

    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1

    return factors


def eulerPhi(n):
    result = n
    for prime in factorize(n):
        result = result // prime * (prime - 1)
    return result


def multiplicativeOrder10(modulus):
    if modulus == 1:
        return 1
    if modulus in ORDER_CACHE:
        return ORDER_CACHE[modulus]
    if math.gcd(10, modulus) != 1:
        ORDER_CACHE[modulus] = None
        return None

    order = eulerPhi(modulus)
    for prime in factorize(order):
        while order % prime == 0 and pow(10, order // prime, modulus) == 1:
            order //= prime

    ORDER_CACHE[modulus] = order
    return order


def digitLengthBounds(a, b, leadingDigit):
    exponent = 0
    power = a
    while power < b:
        power *= 10
        exponent += 1

    low = exponent + 1
    denominator = a * (leadingDigit + 1) - 10 * b
    if denominator <= 0:
        return low, None

    maxPower10 = (b * leadingDigit - 1) // denominator
    if maxPower10 <= 0:
        return None, None

    highExponent = 0
    power = 1
    while power * 10 <= maxPower10:
        power *= 10
        highExponent += 1

    return low, highExponent + 1


def shiftedNumberParameters(a, b):
    if a == b:
        return 1, 1, 9 * b

    denominator = 10 * b - a
    if denominator <= 0:
        return None

    best = None
    for leadingDigit in range(1, 10):
        low, high = digitLengthBounds(a, b, leadingDigit)
        if low is None:
            continue

        low = max(low, 2)
        modulus = denominator // math.gcd(denominator, leadingDigit * b)
        order = multiplicativeOrder10(modulus)
        if order is None:
            continue

        digitLength = ((low + order - 1) // order) * order
        if high is not None and digitLength > high:
            continue

        candidate = (digitLength, leadingDigit)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        return None

    digitLength, leadingDigit = best
    return digitLength, leadingDigit, denominator


def NMod(a, b, modulus=MOD):
    common = math.gcd(a, b)
    a //= common
    b //= common

    if a == b:
        return 1

    parameters = shiftedNumberParameters(a, b)
    if parameters is None:
        return 0

    digitLength, leadingDigit, denominator = parameters
    repunit = (pow(10, digitLength, modulus) - 1) % modulus
    return leadingDigit * b * repunit * pow(denominator, modulus - 2, modulus) % modulus


def exactNSmall(a, b):
    common = math.gcd(a, b)
    a //= common
    b //= common

    if a == b:
        return 1

    parameters = shiftedNumberParameters(a, b)
    if parameters is None:
        return 0

    digitLength, leadingDigit, denominator = parameters
    result = leadingDigit * b * (10 ** digitLength - 1) // denominator
    shifted = int(str(result)[1:] + str(result)[0]) if result >= 10 else result
    assert shifted * b == result * a

    return result


def T(limit, modulus=MOD):
    cubes = [n ** 3 for n in range(limit + 1)]
    total = 0

    for u in range(1, limit + 1):
        a = cubes[u]
        for v in range(1, limit + 1):
            if math.gcd(u, v) == 1:
                total = (total + NMod(a, cubes[v], modulus)) % modulus

    return total


def runTests():
    assert exactNSmall(3, 1) == 142857
    assert exactNSmall(1, 10) == 10
    assert NMod(2, 1) == 0
    assert T(3) == 262429173


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = T(200)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
