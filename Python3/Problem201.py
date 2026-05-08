import itertools
import time


def uniqueSubsetSum(squares, subset_size):
    once = [0] * (subset_size + 1)
    multiple = [0] * (subset_size + 1)
    once[0] = 1

    for square in squares:
        for size in range(subset_size, 0, -1):
            incoming_once = once[size - 1] << square
            incoming_multiple = multiple[size - 1] << square

            multiple[size] = (
                multiple[size]
                | incoming_multiple
                | (once[size] & incoming_once)
            )
            once[size] = (once[size] ^ incoming_once) & ~multiple[size]

    bits = once[subset_size]
    total = 0
    while bits:
        lowest_bit = bits & -bits
        total += lowest_bit.bit_length() - 1
        bits ^= lowest_bit

    return total


def bruteUniqueSubsetSum(squares, subset_size):
    counts = {}
    for subset in itertools.combinations(squares, subset_size):
        total = sum(subset)
        counts[total] = counts.get(total, 0) + 1

    return sum(total for total, count in counts.items() if count == 1)


def runTests():
    squares = [number * number for number in range(1, 6)]
    assert uniqueSubsetSum(squares, 2) == bruteUniqueSubsetSum(squares, 2)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = uniqueSubsetSum([number * number for number in range(1, 101)], 50)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
