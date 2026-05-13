import math
import time


PROBLEM_LIMIT = 10**6


def C_3_1():
    return {(3, 0), (-1, 2), (-1, 0), (-1, -2)}


def S(points):
    return sum(abs(x) + abs(y) for x, y in points)


def mobiusAndPhi(limit):
    mu = [0] * (limit + 1)
    phi = [0] * (limit + 1)
    mu[1] = 1
    phi[1] = 1

    isComposite = bytearray(limit + 1)
    primes = []

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            mu[number] = -1
            phi[number] = number - 1

        for prime in primes:
            composite = number * prime
            if composite > limit:
                break

            isComposite[composite] = 1
            if number % prime == 0:
                mu[composite] = 0
                phi[composite] = phi[number] * prime
                break

            mu[composite] = -mu[number]
            phi[composite] = phi[number] * (prime - 1)

    return mu, phi


def buildB(limit, mu):
    values = [0] * (limit + 1)

    for divisor in range(1, limit + 1):
        if mu[divisor]:
            coefficient = mu[divisor] * divisor

            for p in range(divisor, limit + 1, divisor):
                terms = (p - 1) // (2 * divisor)
                values[p] += coefficient * terms * (terms + 1) // 2

    return values


def gaussianPower(real, imaginary, exponent):
    resultReal, resultImaginary = 1, 0

    for _ in range(exponent):
        resultReal, resultImaginary = (
            resultReal * real - resultImaginary * imaginary,
            resultReal * imaginary + resultImaginary * real,
        )

    return resultReal, resultImaginary


def requiredScaleDenominator(p, q, real, imaginary, denominator):
    e = p - q
    qPowerReal, qPowerImaginary = gaussianPower(real, imaginary, q)
    ePowerReal, ePowerImaginary = gaussianPower(real, -imaginary, e)

    denominatorGap = denominator ** (e - q)
    xNumerator = e * qPowerReal * denominatorGap + q * ePowerReal
    yNumerator = e * qPowerImaginary * denominatorGap + q * ePowerImaginary
    commonDenominator = denominator**e
    commonFactor = math.gcd(commonDenominator, math.gcd(xNumerator, yNumerator))

    return (
        commonDenominator // commonFactor,
        xNumerator // commonFactor,
        yNumerator // commonFactor,
    )


def signedAndSwapped(a, b):
    return [
        (a, b),
        (a, -b),
        (-a, b),
        (-a, -b),
        (b, a),
        (b, -a),
        (-b, a),
        (-b, -a),
    ]


def primitivePythagoreanTriples(maxHypotenuse):
    triples = []
    mLimit = math.isqrt(maxHypotenuse) + 2

    for m in range(2, mLimit + 1):
        for n in range(1, m):
            if (m - n) % 2 == 0 or math.gcd(m, n) != 1:
                continue

            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            if c <= maxHypotenuse:
                triples.append((a, b, c))

    return triples


def baseContribution(limit):
    mu, phi = mobiusAndPhi(limit)
    bValues = buildB(limit, mu)
    total = 0

    # Write R=g*p, r=g*q with gcd(p,q)=1 and q<p/2.  The rational
    # root-of-unity families can be summed over q in closed form; B[p]
    # is the Mobius-inverted correction for the |p-2q| terms.
    for p in range(3, limit + 1):
        coprimeQCount = phi[p] // 2
        if coprimeQCount == 0:
            continue

        if p % 2 == 1:
            inner = 4 * p * coprimeQCount - 2 * bValues[p]
        elif p % 4 == 0:
            inner = 4 * p * coprimeQCount
        else:
            inner = 4 * p * coprimeQCount - 4 * bValues[p]

        scaleLimit = limit // p
        total += inner * scaleLimit * (scaleLimit + 1) // 2

    return total


def pythagoreanCorrection(limit):
    maxHypotenuse = math.isqrt(limit // 3) + 2
    triples = primitivePythagoreanTriples(maxHypotenuse)
    total = 0

    # Nontrivial rational points on the unit circle have Pythagorean
    # denominators.  For p>=13 the denominator needed to make integer
    # coordinates already exceeds floor(limit/p), so only small p remain.
    for p in range(3, min(limit, 12) + 1):
        scaleLimit = limit // p

        for q in range(1, (p + 1) // 2):
            if math.gcd(p, q) != 1:
                continue

            for a, b, denominator in triples:
                for real, imaginary in signedAndSwapped(a, b):
                    requiredScale, x, y = requiredScaleDenominator(
                        p, q, real, imaginary, denominator
                    )

                    if requiredScale <= scaleLimit:
                        scaleMultiplier = scaleLimit // requiredScale
                        total += (
                            (abs(x) + abs(y))
                            * scaleMultiplier
                            * (scaleMultiplier + 1)
                            // 2
                        )

    return total


def T(limit):
    return baseContribution(limit) + pythagoreanCorrection(limit)


def runTests():
    assert S(C_3_1()) == 10
    assert T(3) == 10
    assert T(10) == 524
    assert T(100) == 580442
    assert T(10**3) == 583108600


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = T(PROBLEM_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
