import time


MODULUS = 1_000_000_007


def rootsOnTheRise(n, modulus=MODULUS):
    total = 0
    for k in range(1, n + 1):
        base = (1 - k * k) % modulus
        if base == 1:
            total += n
        elif base:
            total += base * (pow(base, n, modulus) - 1) * pow(base - 1, -1, modulus)
        total %= modulus
    return total


def runTests():
    assert rootsOnTheRise(4) == 51_160


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rootsOnTheRise(10 ** 6)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
