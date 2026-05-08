import time


TARGET_BITS = {0: 1, 1: 2, 10: 4}


def hexadecimalCount(max_length):
    total = 0

    for length in range(1, max_length + 1):
        counts = [0] * 8

        for digit in range(1, 16):
            counts[TARGET_BITS.get(digit, 0)] += 1

        for _ in range(1, length):
            next_counts = [0] * 8
            for mask, count in enumerate(counts):
                for digit in range(16):
                    next_counts[mask | TARGET_BITS.get(digit, 0)] += count
            counts = next_counts

        total += counts[7]

    return total


def runTests():
    assert hexadecimalCount(2) == 0
    assert hexadecimalCount(3) == 4


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hexadecimalCount(16)
    elapsed = time.time() - start

    print("Found " + format(answer, "X") + " in " + str(elapsed) + " seconds.")
