import time

import numpy as np


MODULUS = 20300713
START = 14025256
TARGET = 2 * 10 ** 15


def blumBlumShubDigits():
    digits = bytearray()
    value = START

    while True:
        digits.extend(str(value).encode("ascii"))
        value = (value * value) % MODULUS

        if value == START:
            break

    result = np.frombuffer(digits, dtype=np.uint8).copy()
    result -= ord("0")
    return result


def minimalStartingPositions(digits):
    period_length = len(digits)
    period_sum = int(digits.sum(dtype=np.uint64))

    doubled_digits = np.concatenate((digits, digits))
    prefix_sums = np.empty(len(doubled_digits) + 1, dtype=np.uint32)
    prefix_sums[0] = 0
    np.cumsum(doubled_digits, dtype=np.uint32, out=prefix_sums[1:])

    best = np.zeros(period_sum, dtype=np.uint16)
    best[0] = 1
    remaining = period_sum - 1

    for start in range(period_length):
        sums = prefix_sums[start + 1:start + period_length] - prefix_sums[start]
        cutoff = np.searchsorted(sums, period_sum, side="left")
        sums = sums[:cutoff]

        unseen = sums[best[sums] == 0]
        if unseen.size == 0:
            continue

        keep = np.empty(unseen.size, dtype=bool)
        keep[0] = True
        keep[1:] = unseen[1:] != unseen[:-1]
        newly_seen = unseen[keep]

        if start + 1 > np.iinfo(best.dtype).max:
            raise OverflowError("minimal starting position storage is too small")

        best[newly_seen] = start + 1
        remaining -= int(newly_seen.size)

        if remaining == 0:
            return best

    raise RuntimeError("failed to find every residue")


def sumMinimalPositions(limit, best):
    period_sum = len(best)
    full_periods, remainder = divmod(limit, period_sum)

    return (
        full_periods * int(best.sum(dtype=np.uint64))
        + int(best[1:remainder + 1].sum(dtype=np.uint64))
    )


def runTests(digits, best):
    assert len(digits) == 18886117
    assert int(digits.sum(dtype=np.uint64)) == 80846691
    assert int(best.max()) == 89
    assert sumMinimalPositions(1000, best) == 4742


if __name__ == "__main__":
    start = time.time()
    digits = blumBlumShubDigits()
    best = minimalStartingPositions(digits)
    runTests(digits, best)
    answer = sumMinimalPositions(TARGET, best)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
