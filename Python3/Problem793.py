import time


MODULUS = 50_515_093
SEED = 290_797


def sequence(n):
    value = SEED
    values = []
    for _ in range(n):
        values.append(value)
        value = value * value % MODULUS
    values.sort()
    return values


def countProductsAtMost(values, threshold):
    count = 0
    right = len(values) - 1

    for left, value in enumerate(values):
        while right > left and value * values[right] > threshold:
            right -= 1
        if right <= left:
            break
        count += right - left

    return count


def medianProduct(n):
    values = sequence(n)
    pairCount = n * (n - 1) // 2
    targetRank = (pairCount + 1) // 2

    low = values[0] * values[1]
    high = values[-2] * values[-1]

    while low < high:
        middle = (low + high) // 2
        if countProductsAtMost(values, middle) >= targetRank:
            high = middle
        else:
            low = middle + 1

    return low


def runTests():
    assert medianProduct(3) == 3_878_983_057_768
    assert medianProduct(103) == 492_700_616_748_525


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = medianProduct(1_000_003)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
