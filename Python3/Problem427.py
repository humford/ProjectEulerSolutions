from array import array
from itertools import product
import time


MODULUS = 1_000_000_009


def longestRun(sequence):
    best = 1
    current = 1

    for index in range(1, len(sequence)):
        if sequence[index] == sequence[index - 1]:
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best


def bruteF(n):
    return sum(longestRun(sequence) for sequence in product(range(1, n + 1), repeat=n))


def precomputeWeights(n, modulus):
    factorials = array("I", [1]) * (n + 1)
    for value in range(1, n + 1):
        factorials[value] = factorials[value - 1] * value % modulus

    inverseFactorials = array("I", [1]) * (n + 1)
    inverseFactorials[n] = pow(factorials[n], modulus - 2, modulus)
    for value in range(n, 0, -1):
        inverseFactorials[value - 1] = inverseFactorials[value] * value % modulus

    baseWeights = array("I", [1]) * (n + 1)
    jumpWeights = array("I", [1]) * (n + 1)
    powerN = 1
    powerJump = 1
    jumpBase = (1 - n) % modulus

    for value in range(n + 1):
        baseWeights[value] = powerN * inverseFactorials[value] % modulus
        jumpWeights[value] = powerJump * inverseFactorials[value] % modulus
        powerN = powerN * n % modulus
        powerJump = powerJump * jumpBase % modulus

    return factorials, baseWeights, jumpWeights


def fMod(n, modulus=MODULUS):
    factorials, baseWeights, jumpWeights = precomputeWeights(n, modulus)
    answer = pow(n, n + 1, modulus)

    for forbiddenLength in range(1, n + 1):
        corrected = 0
        remaining = n - forbiddenLength
        jumps = 0

        while remaining >= 0:
            corrected += (
                baseWeights[remaining]
                * jumpWeights[jumps]
                % modulus
                * factorials[remaining + jumps]
                % modulus
            )
            remaining -= forbiddenLength
            jumps += 1

        uncorrected = 0
        remaining = n
        jumps = 0

        while remaining >= 0:
            uncorrected += (
                baseWeights[remaining]
                * jumpWeights[jumps]
                % modulus
                * factorials[remaining + jumps]
                % modulus
            )
            remaining -= forbiddenLength
            jumps += 1

        answer += corrected % modulus - uncorrected % modulus
        if forbiddenLength & 1023 == 0:
            answer %= modulus

    return answer % modulus


def runTests():
    assert bruteF(3) == 45
    assert fMod(3) == 45
    assert fMod(7) == 1403689
    assert fMod(11) == 481496895121 % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fMod(7_500_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
