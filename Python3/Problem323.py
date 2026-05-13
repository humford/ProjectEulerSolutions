import time


BITS = 32


def expectedOrCompletion(bits=BITS):
    total = 0.0
    term = 1.0
    attempts = 0

    while term > 1e-15:
        term = 1.0 - (1.0 - 2.0 ** (-attempts)) ** bits
        total += term
        attempts += 1

    return total


def runTests():
    assert abs(expectedOrCompletion(1) - 2.0) < 1e-12


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.10f}".format(expectedOrCompletion())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
