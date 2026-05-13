import time


LIMIT = 10**18
MODULUS = 7**9


def simulateMoves(bowls):
    beans = [1] * bowls
    position = 0
    moves = 0

    while True:
        amount = beans[position]
        beans[position] = 0

        for _ in range(amount):
            position = (position + 1) % bowls
            beans[position] += 1

        moves += 1

        if all(count == 1 for count in beans):
            return moves


def sequenceMoveCount(exponent):
    return 4**exponent - 3**exponent + 2 ** (exponent + 1)


def gatheringBeansSum(limit=LIMIT, modulus=MODULUS):
    inverse2 = pow(2, -1, modulus)
    inverse3 = pow(3, -1, modulus)

    sum4 = (pow(4, limit + 1, modulus) - 1) * inverse3
    sum3 = (pow(3, limit + 1, modulus) - 1) * inverse2
    sum2 = 2 * (pow(2, limit + 1, modulus) - 1)

    return (sum4 - sum3 + sum2) % modulus


def runTests():
    assert simulateMoves(5) == 15
    assert simulateMoves(100) == 10920
    assert sequenceMoveCount(2) == 15


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = gatheringBeansSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
