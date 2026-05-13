import math
import time


EULER_GAMMA = 0.577215664901532860606512090082402431
DIRECT_LIMIT = 200


def gameAExpected(n):
    return sum(math.comb(n, k) / (k * 2 ** n) for k in range(1, n + 1))


def gameBExpected(n):
    return sum(1 / (k * math.comb(n, k)) for k in range(1, n + 1))


def harmonicNumber(n):
    inverse = 1 / n
    inverse2 = inverse * inverse
    return (
        math.log(n)
        + EULER_GAMMA
        + inverse / 2
        - inverse2 / 12
        + inverse2 * inverse2 / 120
        - inverse2 * inverse2 * inverse2 / 252
        + inverse2 ** 4 / 240
    )


def gameBExpectedFast(n):
    total = 0.0
    weight = 1.0
    for offset in range(min(n, 200)):
        term = weight / (n - offset)
        total += term
        if term < 1e-20:
            break
        weight /= 2
    return total


def reciprocalGameSumValue(limit):
    if limit <= DIRECT_LIMIT:
        return sum(gameAExpected(n) + gameBExpected(n) for n in range(1, limit + 1))

    # The omitted tail of sum(2^-n H_n) is less than 2^-limit * (H_limit + 2),
    # so it is far below the requested eight decimals for the problem input.
    return 4 * harmonicNumber(limit) - 2 * math.log(2) - 2 * gameBExpectedFast(limit)


def reciprocalGameSum(limit):
    return "{:.8f}".format(reciprocalGameSumValue(limit))


def runTests():
    assert "{:.8f}".format(gameAExpected(6)) == "0.39505208"
    assert "{:.8f}".format(gameBExpected(6)) == "0.43333333"
    assert reciprocalGameSum(6) == "7.58932292"
    assert reciprocalGameSum(123_456_789) == "75.44817535"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = reciprocalGameSum(123_456_789)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
