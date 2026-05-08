import time


ALL_DIGITS = (1 << 10) - 1


def pandigitalStepNumbers(max_digits):
    counts = {(digit, 1 << digit): 1 for digit in range(1, 10)}
    total = 0

    for length in range(1, max_digits + 1):
        total += sum(
            count for (digit, mask), count in counts.items() if mask == ALL_DIGITS
        )

        next_counts = {}
        for (digit, mask), count in counts.items():
            for next_digit in (digit - 1, digit + 1):
                if 0 <= next_digit <= 9:
                    key = (next_digit, mask | (1 << next_digit))
                    next_counts[key] = next_counts.get(key, 0) + count
        counts = next_counts

    return total


def runTests():
    assert pandigitalStepNumbers(9) == 0
    assert pandigitalStepNumbers(10) == 1


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pandigitalStepNumbers(40)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
