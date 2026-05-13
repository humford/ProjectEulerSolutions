import time


MODULUS = 1_000_000_007


def gridGraphComponentSum(height, width):
    if height <= 0 or width <= 0:
        raise ValueError("height and width must be positive")

    powHeight = pow(2, height, MODULUS)
    powWidth = pow(2, width, MODULUS)

    term1 = 9 * powHeight * powWidth
    term2 = 2 * height * width * (powHeight + powWidth + 1)
    term3 = -8 * (width * powHeight + height * powWidth)
    term4 = -10 * (powHeight + powWidth)
    term5 = 10 * (height + width + 1)

    return (term1 + term2 + term3 + term4 + term5) % MODULUS


def runTests():
    assert gridGraphComponentSum(3, 3) == 408
    assert gridGraphComponentSum(3, 6) == 4_696
    assert gridGraphComponentSum(10, 20) == 988_971_143


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gridGraphComponentSum(10_000, 20_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
