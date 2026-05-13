import math
import time


INDEX = 10**9
MODULUS = 77777777
PRIME_FACTORS = [7, 11, 73, 101, 137]


def dModPrime(prime, index):
    if index >= prime:
        index = prime + (index - prime) % (prime * (prime - 1))

    maxBlock = index // prime
    targetDigit = index % prime

    binomial = [[0] * prime for _ in range(prime)]
    for row in range(prime):
        binomial[row][0] = 1
        binomial[row][row] = 1

        for column in range(1, row):
            binomial[row][column] = (
                binomial[row - 1][column - 1] + binomial[row - 1][column]
            ) % prime

    factorials = [1] * prime
    for number in range(1, prime):
        factorials[number] = factorials[number - 1] * number % prime

    transformedRows = []
    targetRow = None

    for block in range(maxBlock + 1):
        rowValues = [0] * prime
        digitLimit = targetDigit if block == maxBlock else prime - 1

        for digit in range(digitLimit + 1):
            previousBlocks = 0

            for previousBlock in range(block):
                previousBlocks = (
                    previousBlocks
                    + binomial[block][previousBlock]
                    * transformedRows[previousBlock][digit]
                ) % prime

            currentBlock = 0
            for previousDigit in range(digit):
                currentBlock = (
                    currentBlock
                    + binomial[digit][previousDigit] * rowValues[previousDigit]
                ) % prime

            rowValues[digit] = (
                (factorials[digit] if block == 0 else 0)
                + previousBlocks
                + currentBlock
            ) % prime

        if block == maxBlock:
            targetRow = rowValues
            break

        transformed = [0] * prime
        for digit in range(prime):
            transformed[digit] = sum(
                binomial[digit][previousDigit] * rowValues[previousDigit]
                for previousDigit in range(digit + 1)
            ) % prime

        transformedRows.append(transformed)

    return targetRow[targetDigit]


def chineseRemainder(residues, moduli):
    result = 0
    product = 1

    for residue, modulus in zip(residues, moduli):
        adjustment = ((residue - result) % modulus) * pow(product, -1, modulus)
        adjustment %= modulus
        result += product * adjustment
        product *= modulus

    return result % product


def exactD(index):
    values = [0] * (index + 1)

    for number in range(index + 1):
        total = math.factorial(number)

        for previous in range(number):
            total += math.comb(number, previous) * values[previous]

        values[number] = total

    return values[index]


def eulerNumberCoefficientSum(index=INDEX):
    residues = []

    for prime in PRIME_FACTORS:
        dValue = dModPrime(prime, index)

        if index >= prime:
            residues.append((-dValue) % prime)
        else:
            residues.append((math.factorial(index) - dValue) % prime)

    return chineseRemainder(residues, PRIME_FACTORS)


def runTests():
    d10 = exactD(10)
    assert d10 == 328161643
    assert math.factorial(10) - 2 * d10 == -652694486
    assert eulerNumberCoefficientSum(10) == (math.factorial(10) - d10) % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = eulerNumberCoefficientSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
