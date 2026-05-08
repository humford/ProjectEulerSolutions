import time


def isBouncy(n):
    digits = [int(digit) for digit in str(n)]
    increasing = all(a <= b for a, b in zip(digits, digits[1:]))
    decreasing = all(a >= b for a, b in zip(digits, digits[1:]))
    return not increasing and not decreasing


def leastBouncyProportion(numerator, denominator):
    bouncy_count = 0
    n = 0

    while True:
        n += 1
        if isBouncy(n):
            bouncy_count += 1
        if bouncy_count * denominator == numerator * n:
            return n


def runTests():
    assert isBouncy(155349)
    assert not isBouncy(134468)
    assert not isBouncy(66420)
    assert leastBouncyProportion(1, 2) == 538
    assert leastBouncyProportion(9, 10) == 21780


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = leastBouncyProportion(99, 100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
