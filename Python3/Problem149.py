import time
from array import array


def laggedFibonacciValues(count):
    values = array("i")

    for k in range(1, count + 1):
        if k <= 55:
            value = (100003 - 200003 * k + 300007 * k ** 3) % 1000000 - 500000
        else:
            value = (values[k - 25] + values[k - 56] + 1000000) % 1000000 - 500000
        values.append(value)

    return values


def maxSubsequenceSum(sequence):
    best = None
    current = 0

    for value in sequence:
        current = value if current <= 0 else current + value
        best = current if best is None else max(best, current)

    return best


def maximumGridSubsequence(size):
    grid = laggedFibonacciValues(size * size)
    best = -10 ** 18

    for row in range(size):
        best = max(best, maxSubsequenceSum(grid[row * size : (row + 1) * size]))

    for col in range(size):
        best = max(best, maxSubsequenceSum(grid[row * size + col] for row in range(size)))

    for start_col in range(size):
        best = max(
            best,
            maxSubsequenceSum(
                grid[row * size + start_col + row]
                for row in range(size - start_col)
            ),
        )
    for start_row in range(1, size):
        best = max(
            best,
            maxSubsequenceSum(
                grid[(start_row + offset) * size + offset]
                for offset in range(size - start_row)
            ),
        )

    for start_col in range(size):
        best = max(
            best,
            maxSubsequenceSum(
                grid[row * size + start_col - row]
                for row in range(start_col + 1)
            ),
        )
    for start_row in range(1, size):
        best = max(
            best,
            maxSubsequenceSum(
                grid[(start_row + offset) * size + size - 1 - offset]
                for offset in range(size - start_row)
            ),
        )

    return best


def runTests():
    values = laggedFibonacciValues(100)
    assert values[9] == -393027
    assert values[99] == 86613


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumGridSubsequence(2000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
