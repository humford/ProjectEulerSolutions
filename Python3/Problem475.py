import time


MODULUS = 1_000_000_007
PROBLEM_MUSICIANS = 600


def prepareFactorials(limit):
    factorials = [1] * (limit + 1)
    for value in range(1, limit + 1):
        factorials[value] = factorials[value - 1] * value % MODULUS

    inverseFactorials = [1] * (limit + 1)
    inverseFactorials[limit] = pow(factorials[limit], MODULUS - 2, MODULUS)
    for value in range(limit, 0, -1):
        inverseFactorials[value - 1] = (
            inverseFactorials[value] * value % MODULUS
        )

    return factorials, inverseFactorials


def powers(base, count):
    values = [1] * (count + 1)
    for index in range(1, count + 1):
        values[index] = values[index - 1] * base % MODULUS
    return values


def trioArrangementCount(musicians):
    if musicians % 12 != 0:
        raise ValueError("musician count must be a multiple of 12")

    n = musicians // 12
    trioCount = 4 * n
    quartetCount = 3 * n
    factorials, inverseFactorials = prepareFactorials(16 * n + 10)
    powers2 = powers(2, trioCount)
    powersNegative3 = powers(MODULUS - 3, trioCount)
    inverse2Powers = powers((MODULUS + 1) // 2, trioCount)
    inverse24Powers = powers(pow(24, MODULUS - 2, MODULUS), quartetCount)

    sigma = 0
    for i in range(trioCount + 1):
        for j in range(trioCount - i + 1):
            k = trioCount - i - j
            edgeCount = 3 * i + j
            base = factorials[edgeCount] * inverseFactorials[i] % MODULUS
            base = base * powersNegative3[j] % MODULUS
            base = base * powers2[k] % MODULUS

            minD = max(0, n - i)
            maxD = j // 2
            if minD > maxD:
                continue

            dSum = 0
            for d in range(minD, maxD + 1):
                a = i - n + d
                b = j - 2 * d
                term = inverseFactorials[a]
                term = term * inverseFactorials[b] % MODULUS
                term = term * inverseFactorials[k] % MODULUS
                term = term * inverseFactorials[d] % MODULUS
                term = term * inverse24Powers[a] % MODULUS
                term = term * inverse2Powers[b + d] % MODULUS
                dSum = (dSum + term) % MODULUS

            sigma = (sigma + base * dSum) % MODULUS

    answer = pow(24, quartetCount, MODULUS)
    answer = answer * factorials[quartetCount] % MODULUS
    answer = answer * sigma % MODULUS
    answer = answer * pow(pow(6, trioCount, MODULUS), MODULUS - 2, MODULUS)
    return answer % MODULUS


def runTests():
    assert trioArrangementCount(12) == 576
    assert trioArrangementCount(24) == 509_089_824


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = trioArrangementCount(PROBLEM_MUSICIANS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
