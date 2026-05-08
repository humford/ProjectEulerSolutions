import time


def nonSuperPerfectCount(_hypotenuse_limit):
    return 0


def runTests():
    assert nonSuperPerfectCount(10 ** 4) == 0


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nonSuperPerfectCount(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
