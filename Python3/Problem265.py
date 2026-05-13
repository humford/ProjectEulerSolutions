import time


BITS = 5


def binaryCircleSum(bits):
    mask = (1 << bits) - 1
    all_seen = (1 << (1 << bits)) - 1

    def search(seen, sequence):
        if seen == all_seen:
            return sequence >> (bits - 1)

        prefix = (sequence << 1) & mask
        result = 0

        for bit in (0, 1):
            value = prefix | bit
            if not (seen >> value) & 1:
                result += search(seen | (1 << value), (sequence << 1) | bit)

        return result

    return search(1, 0)


def runTests():
    assert binaryCircleSum(3) == 52


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = binaryCircleSum(BITS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
