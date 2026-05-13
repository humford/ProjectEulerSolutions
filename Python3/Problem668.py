import math
import time


def primePiTable(limit):
    root = math.isqrt(limit)
    values = sorted(
        set([limit // index for index in range(1, root + 1)] + list(range(1, root + 1))),
        reverse=True,
    )
    primeCounts = {value: value - 1 for value in values}

    for prime in range(2, root + 1):
        if primeCounts[prime] == primeCounts[prime - 1]:
            continue
        previousCount = primeCounts[prime - 1]
        square = prime * prime
        for value in values:
            if value < square:
                break
            primeCounts[value] -= primeCounts[value // prime] - previousCount

    return primeCounts


def primeSumUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * ((limit - start) // prime + 1)
    return sum(number for number in range(limit + 1) if sieve[number])


def squareRootSmoothCount(limit):
    root = math.isqrt(limit)
    primeCounts = primePiTable(limit)

    notSmooth = primeSumUpTo(root)
    for quotient in range(1, root + 1):
        upper = limit // quotient
        lower = max(root, limit // (quotient + 1))
        notSmooth += quotient * (primeCounts[upper] - primeCounts[lower])
    return limit - notSmooth


def runTests():
    assert squareRootSmoothCount(100) == 29
    assert squareRootSmoothCount(1_000) == 274
    assert squareRootSmoothCount(10_000) == 2_656


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squareRootSmoothCount(10_000_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
