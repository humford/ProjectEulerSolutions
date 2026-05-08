import time


def neverDividesTribonacci(modulus):
    a = b = c = 1 % modulus

    while True:
        a, b, c = b, c, (a + b + c) % modulus
        if c == 0:
            return False
        if (a, b, c) == (1 % modulus, 1 % modulus, 1 % modulus):
            return True


def oddNonDivisor(index):
    count = 0
    candidate = 1

    while True:
        candidate += 2
        if neverDividesTribonacci(candidate):
            count += 1
            if count == index:
                return candidate


def runTests():
    assert oddNonDivisor(1) == 27


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = oddNonDivisor(124)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
