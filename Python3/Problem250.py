import itertools
import time


LIMIT = 250250
DIVISOR = 250
MODULUS = 10 ** 16


def divisiblePowerSubsetCount(limit, divisor, modulus):
    counts = [0] * divisor
    counts[0] = 1

    for number in range(1, limit + 1):
        residue = pow(number, number, divisor)
        next_counts = counts[:]

        for total in range(divisor):
            next_counts[(total + residue) % divisor] = (
                next_counts[(total + residue) % divisor] + counts[total]
            ) % modulus

        counts = next_counts

    return (counts[0] - 1) % modulus


def bruteDivisiblePowerSubsetCount(limit, divisor):
    values = [pow(number, number, divisor) for number in range(1, limit + 1)]
    result = 0

    for size in range(1, len(values) + 1):
        for subset in itertools.combinations(values, size):
            if sum(subset) % divisor == 0:
                result += 1

    return result


def runTests():
    assert divisiblePowerSubsetCount(6, 5, MODULUS) == bruteDivisiblePowerSubsetCount(6, 5)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisiblePowerSubsetCount(LIMIT, DIVISOR, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
