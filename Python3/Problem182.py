import math
import time


def unconcealedMessageCount(exponent, p, q):
    return (1 + math.gcd(exponent - 1, p - 1)) * (
        1 + math.gcd(exponent - 1, q - 1)
    )


def minimumUnconcealedExponentSum(p, q):
    phi = (p - 1) * (q - 1)
    best = None
    total = 0

    for exponent in range(2, phi):
        if math.gcd(exponent, phi) != 1:
            continue

        count = unconcealedMessageCount(exponent, p, q)
        if best is None or count < best:
            best = count
            total = exponent
        elif count == best:
            total += exponent

    return total


def runTests():
    assert unconcealedMessageCount(181, 19, 37) == 703


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimumUnconcealedExponentSum(1009, 3643)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
