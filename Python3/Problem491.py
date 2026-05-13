import itertools
import math
import time


def doublePandigitalDivisibleBy11():
    total = 0
    for odd_counts in itertools.product(range(3), repeat=10):
        if sum(odd_counts) != 10:
            continue
        if (2 * sum(digit * odd_counts[digit] for digit in range(10)) - 90) % 11:
            continue

        odd_arrangements = math.factorial(10)
        even_arrangements = math.factorial(10)
        for digit, count in enumerate(odd_counts):
            odd_arrangements //= math.factorial(count)
            even_arrangements //= math.factorial(2 - count)

        subtotal = odd_arrangements * even_arrangements
        if odd_counts[0]:
            bad_odd_arrangements = math.factorial(9) // math.factorial(odd_counts[0] - 1)
            for digit in range(1, 10):
                bad_odd_arrangements //= math.factorial(odd_counts[digit])
            subtotal -= bad_odd_arrangements * even_arrangements
        total += subtotal
    return total


def runTests():
    assert doublePandigitalDivisibleBy11() == 194_505_988_824_000


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = doublePandigitalDivisibleBy11()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
