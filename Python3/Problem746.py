import time


MODULUS = 1_000_000_007


def factorialTables(limit):
    factorials = [1] * (limit + 1)
    for number in range(1, limit + 1):
        factorials[number] = factorials[number - 1] * number % MODULUS

    inverseFactorials = [1] * (limit + 1)
    inverseFactorials[limit] = pow(factorials[limit], MODULUS - 2, MODULUS)
    for number in range(limit, 0, -1):
        inverseFactorials[number - 1] = inverseFactorials[number] * number % MODULUS

    return factorials, inverseFactorials


def modularInverses(limit):
    inverses = [0] * (limit + 1)
    if limit >= 1:
        inverses[1] = 1
    for number in range(2, limit + 1):
        inverses[number] = MODULUS - (MODULUS // number) * inverses[MODULUS % number] % MODULUS
    return inverses


def binomial(n, k, factorials, inverseFactorials):
    if k < 0 or k > n:
        return 0
    return factorials[n] * inverseFactorials[k] % MODULUS * inverseFactorials[n - k] % MODULUS


def dinnerArrangements(n, factorials, inverseFactorials, inverses, powersOfFour):
    if n == 1:
        return 0

    total = 0
    selectedFamilyPermutations = 1

    for selectedFamilies in range(n + 1):
        if selectedFamilies > 0:
            selectedFamilyPermutations = (
                selectedFamilyPermutations * (n - selectedFamilies + 1) % MODULUS
            )

        if selectedFamilies == 0:
            disjointBlocks = 1
        else:
            disjointBlocks = 4 * n % MODULUS
            disjointBlocks = disjointBlocks * inverses[selectedFamilies] % MODULUS
            disjointBlocks = disjointBlocks * binomial(
                4 * n - 3 * selectedFamilies - 1,
                selectedFamilies - 1,
                factorials,
                inverseFactorials,
            ) % MODULUS

        remainingMenOrWomen = 2 * (n - selectedFamilies)
        term = selectedFamilyPermutations
        term = term * disjointBlocks % MODULUS
        term = term * powersOfFour[selectedFamilies] % MODULUS
        term = term * factorials[remainingMenOrWomen] % MODULUS
        term = term * factorials[remainingMenOrWomen] % MODULUS

        if selectedFamilies % 2:
            total -= term
        else:
            total += term
        total %= MODULUS

    return 2 * total % MODULUS


def messyDinnerSum(limit):
    factorials, inverseFactorials = factorialTables(4 * limit)
    inverses = modularInverses(limit)
    powersOfFour = [1] * (limit + 1)
    for index in range(1, limit + 1):
        powersOfFour[index] = powersOfFour[index - 1] * 4 % MODULUS

    return sum(
        dinnerArrangements(n, factorials, inverseFactorials, inverses, powersOfFour)
        for n in range(2, limit + 1)
    ) % MODULUS


def runTests():
    factorials, inverseFactorials = factorialTables(4 * 10)
    inverses = modularInverses(10)
    powersOfFour = [1] * 11
    for index in range(1, 11):
        powersOfFour[index] = powersOfFour[index - 1] * 4 % MODULUS

    assert dinnerArrangements(1, factorials, inverseFactorials, inverses, powersOfFour) == 0
    assert dinnerArrangements(2, factorials, inverseFactorials, inverses, powersOfFour) == 896
    assert dinnerArrangements(3, factorials, inverseFactorials, inverses, powersOfFour) == 890_880
    assert dinnerArrangements(10, factorials, inverseFactorials, inverses, powersOfFour) == 170_717_180
    assert messyDinnerSum(10) == 399_291_975


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = messyDinnerSum(2021)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
