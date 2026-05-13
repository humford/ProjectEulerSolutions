import time


A = 21**7
B = 7**21
C = 12**7
MODULUS = 10**9


def ceilSum(limit, divisor):
    quotient, remainder = divmod(limit, divisor)
    return divisor * quotient * (quotient + 1) // 2 + (quotient + 1) * remainder


def crazyFunctionSum(a, b, c):
    count = b + 1
    blockSum = ceilSum(count, a)
    return (
        b * (b + 1) // 2
        + count * 4 * (a - c)
        + (4 * a - 3 * c) * (blockSum - count)
    )


def runTests():
    assert crazyFunctionSum(50, 2000, 40) == 5204240


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = crazyFunctionSum(A, B, C) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
