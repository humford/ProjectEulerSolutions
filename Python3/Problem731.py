import time


DIGIT_BLOCK_MODULUS = 10**10


def powersOfThreeThrough(limit):
    powers = []
    value = 3
    while value <= limit:
        powers.append(value)
        value *= 3
    return powers


def stonehamDigits(position):
    shiftedPosition = position + 9
    powers = powersOfThreeThrough(shiftedPosition)

    quotientTotal = 0
    remainders = []

    for power in powers:
        modulus = power * DIGIT_BLOCK_MODULUS
        residue = pow(10, shiftedPosition - power, modulus)
        quotientTotal = (quotientTotal + residue // power) % DIGIT_BLOCK_MODULUS
        remainders.append(residue % power)

    commonDenominator = powers[-1]
    carryNumerator = 0
    for remainder, power in zip(remainders, powers):
        carryNumerator += remainder * (commonDenominator // power)

    answer = (quotientTotal + carryNumerator // commonDenominator) % DIGIT_BLOCK_MODULUS
    return str(answer).zfill(10)


def runTests():
    assert stonehamDigits(100) == "4938271604"
    assert stonehamDigits(10**8) == "2584642393"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = stonehamDigits(10**16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
