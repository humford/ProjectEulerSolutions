import time


MODULUS = 1_000_267_129
DIGIT_COUNT = 10
MASK_COUNT = 1 << DIGIT_COUNT


def _digit_mask(n):
    mask = 0
    for digit in str(n):
        mask |= 1 << int(digit)
    return mask


def bruteFriendPairCount(limit):
    masks = [_digit_mask(n) for n in range(1, limit)]
    return sum(
        1
        for left in range(len(masks))
        for right in range(left + 1, len(masks))
        if masks[left] & masks[right]
    )


def maskCountsBelowPowerOfTen(exponent):
    counts = [0] * MASK_COUNT
    current = [0] * MASK_COUNT

    for digit in range(1, DIGIT_COUNT):
        current[1 << digit] += 1

    for _ in range(1, exponent + 1):
        for mask, count in enumerate(current):
            counts[mask] += count

        following = [0] * MASK_COUNT
        for mask, count in enumerate(current):
            if count:
                for digit in range(DIGIT_COUNT):
                    following[mask | (1 << digit)] += count
        current = following

    return counts


def disjointPairCount(maskCounts):
    total = 0
    for leftMask, leftCount in enumerate(maskCounts):
        if not leftCount:
            continue
        for rightMask in range(leftMask + 1, MASK_COUNT):
            if leftMask & rightMask == 0:
                total += leftCount * maskCounts[rightMask]
    return total


def friendPairCount(limit):
    if limit < 1_000:
        return bruteFriendPairCount(limit)

    exponent = 0
    power = 1
    while power < limit:
        power *= 10
        exponent += 1

    if power != limit:
        raise ValueError("this solution handles the problem's powers of ten")

    maskCounts = maskCountsBelowPowerOfTen(exponent)
    numberCount = limit - 1
    allPairs = numberCount * (numberCount - 1) // 2
    return allPairs - disjointPairCount(maskCounts)


def runTests():
    assert _digit_mask(1123) & _digit_mask(3981)
    assert sum(maskCountsBelowPowerOfTen(2)) == 99
    assert friendPairCount(30) == bruteFriendPairCount(30)
    assert friendPairCount(100) == 1_539


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = friendPairCount(10 ** 18) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
