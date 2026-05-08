import time


def isPrime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True


def primeCubePartnershipCount(limit):
    count = 0
    k = 1

    while True:
        p = 3 * k * k + 3 * k + 1
        if p >= limit:
            return count
        if isPrime(p):
            count += 1
        k += 1


def runTests():
    assert primeCubePartnershipCount(100) == 4


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primeCubePartnershipCount(1000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
