import time


MODULUS = 1_000_000_007


def modularInverses(limit):
    inverses = [0] * (limit + 1)
    if limit >= 1:
        inverses[1] = 1
    for value in range(2, limit + 1):
        inverses[value] = (
            MODULUS
            - (MODULUS // value) * inverses[MODULUS % value] % MODULUS
        )
    return inverses


def headCountCoefficient(n, k):
    inverses = modularInverses(k)
    binomial = 1
    total = 0

    for index in range(k + 1):
        term = binomial * pow(k - index, n, MODULUS)
        if index % 2:
            total -= term
        else:
            total += term
        total %= MODULUS

        if index < k:
            binomial = (
                binomial
                * ((n + 1 - index) % MODULUS)
                * inverses[index + 1]
            ) % MODULUS

    return total


def runTests():
    assert headCountCoefficient(3, 1) == 1
    assert headCountCoefficient(3, 2) == 4
    assert headCountCoefficient(3, 3) == 1
    assert headCountCoefficient(100, 40) % MODULUS == 986_699_437


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = headCountCoefficient(10_000_000, 4_000_000) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
