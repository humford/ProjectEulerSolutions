import math
import time


def shortenedBinaryExpansion(numerator, denominator):
    divisor = math.gcd(numerator, denominator)
    numerator //= divisor
    denominator //= divisor

    x, y = denominator, numerator
    reverse_runs = []

    while x != y:
        if x > y:
            count = (x - 1) // y
            reverse_runs.append((1, count))
            x -= count * y
        else:
            count = (y - 1) // x
            reverse_runs.append((0, count))
            y -= count * x

    runs = []
    current_bit = 1
    current_count = 1

    for bit, count in reversed(reverse_runs):
        if bit == current_bit:
            current_count += count
        else:
            runs.append(current_count)
            current_bit = bit
            current_count = count

    runs.append(current_count)
    return ",".join(str(count) for count in runs)


def runTests():
    assert shortenedBinaryExpansion(13, 17) == "4,3,1"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = shortenedBinaryExpansion(123456789, 987654321)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
