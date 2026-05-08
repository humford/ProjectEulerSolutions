import time


def firstPartitionDivisibleBy(modulus):
    partitions = [1]
    n = 1

    while True:
        total = 0
        k = 1

        while True:
            pentagonal_one = k * (3 * k - 1) // 2
            pentagonal_two = k * (3 * k + 1) // 2
            if pentagonal_one > n:
                break

            sign = 1 if k % 2 == 1 else -1
            total += sign * partitions[n - pentagonal_one]
            if pentagonal_two <= n:
                total += sign * partitions[n - pentagonal_two]
            k += 1

        partitions.append(total % modulus)
        if partitions[n] == 0:
            return n
        n += 1


def runTests():
    assert firstPartitionDivisibleBy(5) == 4


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = firstPartitionDivisibleBy(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
