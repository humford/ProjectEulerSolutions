import time


MODULUS = 10 ** 9


def squareDigitSumTotal(length):
    max_sum = 81 * length
    counts = [0] * (max_sum + 1)
    sums = [0] * (max_sum + 1)
    counts[0] = 1

    for _ in range(length):
        next_counts = [0] * (max_sum + 1)
        next_sums = [0] * (max_sum + 1)

        for current_sum, count in enumerate(counts):
            if count == 0:
                continue
            current_value_sum = sums[current_sum]
            for digit in range(10):
                new_sum = current_sum + digit * digit
                next_counts[new_sum] += count
                next_sums[new_sum] = (
                    next_sums[new_sum] + current_value_sum * 10 + digit * count
                ) % MODULUS

        counts = next_counts
        sums = next_sums

    squares = {n * n for n in range(0, int(max_sum ** 0.5) + 1)}
    return sum(sums[value] for value in squares) % MODULUS


def bruteSquareDigitSumTotal(length):
    total = 0
    max_sum = 81 * length
    squares = {n * n for n in range(0, int(max_sum ** 0.5) + 1)}
    for n in range(10 ** length):
        if sum(int(digit) ** 2 for digit in str(n)) in squares:
            total += n
    return total % MODULUS


def runTests():
    assert squareDigitSumTotal(2) == bruteSquareDigitSumTotal(2)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squareDigitSumTotal(20)
    elapsed = time.time() - start

    print("Found " + str(answer).zfill(9) + " in " + str(elapsed) + " seconds.")
