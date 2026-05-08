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


def runTests():
    assert blockCombinations(7, 3) == 17


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = blockCombinations(50, 3)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
