import math
import time
from fractions import Fraction


def bernoulliNumbers(limit):
    values = [Fraction(0) for _ in range(limit + 1)]
    result = [Fraction(0) for _ in range(limit + 1)]

    for index in range(limit + 1):
        values[index] = Fraction(1, index + 1)
        for reverseIndex in range(index, 0, -1):
            values[reverseIndex - 1] = reverseIndex * (
                values[reverseIndex - 1] - values[reverseIndex]
            )
        result[index] = values[0]

    return result


def divisorPowerSums(limit, power):
    sums = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        divisorPower = divisor**power
        for multiple in range(divisor, limit + 1, divisor):
            sums[multiple] += divisorPower
    return sums


def directE(power, q, tolerance=1e-15):
    total = 0.0
    index = 1
    sieveLimit = 512
    sigma = divisorPowerSums(sieveLimit, power)
    qPower = q

    while True:
        if index > sieveLimit:
            sieveLimit *= 2
            sigma = divisorPowerSums(sieveLimit, power)

        term = float(sigma[index]) * qPower
        total += term

        scale = max(1.0, abs(total))
        if index >= 50 and abs(term) < tolerance * scale:
            nextQPower = qPower * q
            tailIsSmall = True
            for offset in range(1, 6):
                tailIndex = index + offset
                if tailIndex > sieveLimit:
                    sieveLimit *= 2
                    sigma = divisorPowerSums(sieveLimit, power)

                tailTerm = float(sigma[tailIndex]) * nextQPower
                if abs(tailTerm) >= tolerance * scale:
                    tailIsSmall = False
                    break
                nextQPower *= q

            if tailIsSmall:
                return total

        index += 1
        qPower *= q


def oddPowerE(power, q):
    if power % 2 == 0 or power < 3:
        raise ValueError("power must be odd and at least 3")

    r = (power + 1) // 2
    bernoulli = bernoulliNumbers(2 * r)[2 * r]
    constant = ((-1) ** (r + 1)) * bernoulli / (4 * r)

    t = -math.log1p(-(1.0 - q)) / (2.0 * math.pi)
    tPower = t ** (-2 * r)

    exponent = 2.0 * math.pi / t
    if exponent > 745.0:
        transformedSeries = 0.0
    else:
        transformedQ = math.exp(-exponent)
        transformedSeries = directE(power, transformedQ, tolerance=1e-18)

    return tPower * transformedSeries + (tPower - 1.0) * float(constant)


def scientific12(value):
    mantissa, exponent = f"{value:.12e}".split("e")
    return mantissa + "e" + str(int(exponent))


def slowlyConvergingSeries(power, denominatorPower):
    q = 1.0 - 1.0 / (2.0**denominatorPower)
    if power == 1:
        value = directE(power, q, tolerance=1e-16)
    else:
        value = oddPowerE(power, q)
    return scientific12(value)


def runTests():
    assert slowlyConvergingSeries(1, 4) == "3.872155809243e2"
    assert slowlyConvergingSeries(3, 8) == "2.767385314772e10"
    assert slowlyConvergingSeries(7, 15) == "6.725803486744e39"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = slowlyConvergingSeries(15, 25)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
