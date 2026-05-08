import time


PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]


def leastNWithSolutionsAbove(target):
    required_divisors = 2 * target - 1
    best = 10 ** 30

    def search(index, max_exponent, current, divisor_count):
        nonlocal best

        if divisor_count > required_divisors:
            best = min(best, current)
            return
        if index == len(PRIMES):
            return

        value = current
        for exponent in range(1, max_exponent + 1):
            value *= PRIMES[index]
            if value >= best:
                break
            search(index + 1, exponent, value, divisor_count * (2 * exponent + 1))

    search(0, 64, 1, 1)
    return best


def runTests():
    assert leastNWithSolutionsAbove(4) == 6


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastNWithSolutionsAbove(1000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
