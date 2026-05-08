import itertools
import time


def subsetIndexes(mask, n):
    return [index for index in range(n) if mask & (1 << index)]


def requiresEqualityTest(first, second):
    return not (
        all(a < b for a, b in zip(first, second))
        or all(a > b for a, b in zip(first, second))
    )


def subsetPairTestCount(n):
    masks_by_size = {}
    for mask in range(1, 1 << n):
        size = mask.bit_count()
        if size >= 2:
            masks_by_size.setdefault(size, []).append(mask)

    count = 0
    for size, masks in masks_by_size.items():
        for first_index, first_mask in enumerate(masks):
            first = subsetIndexes(first_mask, n)
            for second_mask in masks[first_index + 1 :]:
                if first_mask & second_mask:
                    continue
                second = subsetIndexes(second_mask, n)
                if requiresEqualityTest(first, second):
                    count += 1

    return count


def runTests():
    assert subsetPairTestCount(4) == 1
    assert subsetPairTestCount(7) == 70


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = subsetPairTestCount(12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
