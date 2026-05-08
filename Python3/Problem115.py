import functools
import time


def blockCombinations(length, minimum_block):
    @functools.lru_cache(maxsize=None)
    def count(remaining_length):
        total = 1

        for start in range(remaining_length - minimum_block + 1):
            for block_length in range(minimum_block, remaining_length - start + 1):
                after_block = remaining_length - start - block_length - 1
                total += count(after_block) if after_block >= 0 else 1

        return total

    return count(length)


def leastLengthExceeding(minimum_block, threshold):
    length = minimum_block
    while blockCombinations(length, minimum_block) <= threshold:
        length += 1
    return length


def runTests():
    assert leastLengthExceeding(3, 1000000) == 30


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastLengthExceeding(50, 1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
