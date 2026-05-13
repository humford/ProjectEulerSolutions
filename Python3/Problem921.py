from math import isqrt
import time


MODULUS = 398_874_989
TARGET_M = 1_618_034


def factorization(n):
    factors = {}
    factor = 2

    while factor * factor <= n:
        if n % factor == 0:
            exponent = 0
            while n % factor == 0:
                n //= factor
                exponent += 1
            factors[factor] = exponent
        factor += 1 if factor == 2 else 2

    if n > 1:
        factors[n] = 1

    return factors


def modularSquareRoot(n, prime):
    if n == 0:
        return 0
    if prime == 2:
        return n
    if pow(n, (prime - 1) // 2, prime) != 1:
        raise ValueError("not a quadratic residue")
    if prime % 4 == 3:
        return pow(n, (prime + 1) // 4, prime)

    q = prime - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    z = 2
    while pow(z, (prime - 1) // 2, prime) != prime - 1:
        z += 1

    m = s
    c = pow(z, q, prime)
    t = pow(n, q, prime)
    r = pow(n, (q + 1) // 2, prime)

    while t != 1:
        i = 1
        value = pow(t, 2, prime)
        while value != 1:
            value = pow(value, 2, prime)
            i += 1

        b = pow(c, 1 << (m - i - 1), prime)
        m = i
        c = b * b % prime
        t = t * c % prime
        r = r * b % prime

    return r


def multiplicativeOrder(value, prime):
    order = prime - 1
    for factor, exponent in factorization(prime - 1).items():
        for _ in range(exponent):
            if order % factor == 0 and pow(value, order // factor, prime) == 1:
                order //= factor
            else:
                break
    return order


def sequenceParameters():
    sqrt5 = modularSquareRoot(5, MODULUS)
    alpha = (2 + sqrt5) % MODULUS
    beta = (2 - sqrt5) % MODULUS
    order = multiplicativeOrder(alpha, MODULUS)
    inverseTwo = pow(2, -1, MODULUS)
    inverseTwoSqrt5 = pow(2 * sqrt5, -1, MODULUS)

    return sqrt5, alpha, beta, order, inverseTwo, inverseTwoSqrt5


SQRT5, ALPHA, BETA, ALPHA_ORDER, INVERSE_TWO, INVERSE_TWO_SQRT5 = sequenceParameters()


# The recurrence is the formula for coth(5x).  Since
# phi = coth(u) with exp(2u) = 2 + sqrt(5), we have
#
#     a_n = coth(5^n u)
#         = ((2 + sqrt(5))^(5^n) + 1) / ((2 + sqrt(5))^(5^n) - 1).
#
# If (2 + sqrt(5))^(5^n) = q_n + p_n sqrt(5), then the displayed form in
# the problem is exactly a_n = (p_n sqrt(5) + 1) / q_n.


def sFromPowerExponent(exponent):
    alphaPower = pow(ALPHA, exponent, MODULUS)
    betaPower = pow(BETA, exponent, MODULUS)
    q = (alphaPower + betaPower) * INVERSE_TWO % MODULUS
    p = (alphaPower - betaPower) * INVERSE_TWO_SQRT5 % MODULUS

    return (pow(p, 5, MODULUS) + pow(q, 5, MODULUS)) % MODULUS


def s(n):
    return sFromPowerExponent(pow(5, n, ALPHA_ORDER))


def S(m):
    if m < 2:
        return 0

    previousExponent = 5 % ALPHA_ORDER
    currentExponent = 5 % ALPHA_ORDER
    total = 0

    for _ in range(2, m + 1):
        total = (total + sFromPowerExponent(currentExponent)) % MODULUS
        previousExponent, currentExponent = (
            currentExponent,
            previousExponent * currentExponent % ALPHA_ORDER,
        )

    return total


def multiplyQuadratic(left, right):
    leftQ, leftP = left
    rightQ, rightP = right
    return (
        leftQ * rightQ + 5 * leftP * rightP,
        leftQ * rightP + leftP * rightQ,
    )


def directS(n):
    exponent = 5**n
    result = (1, 0)
    base = (2, 1)

    while exponent:
        if exponent % 2 == 1:
            result = multiplyQuadratic(result, base)
        base = multiplyQuadratic(base, base)
        exponent //= 2

    q, p = result
    return (p**5 + q**5) % MODULUS


def solve():
    return S(TARGET_M)


def runTests():
    assert MODULUS > 2
    assert all(MODULUS % n for n in range(2, isqrt(MODULUS) + 1))
    assert SQRT5 * SQRT5 % MODULUS == 5
    assert s(0) == 33
    assert s(0) == directS(0)
    assert s(1) == directS(1)
    assert s(2) == directS(2)
    assert S(2) == s(1)
    assert S(3) == (s(1) + s(2)) % MODULUS
    assert solve() == 378_401_935


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
