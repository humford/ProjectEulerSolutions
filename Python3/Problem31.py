def coinSums(total, coins):
    ways = [0] * (total + 1)
    ways[0] = 1

    for coin in coins:
        for value in range(coin, total + 1):
            ways[value] += ways[value - coin]

    return ways[total]


def runTests():
    assert coinSums(5, [1, 2, 5]) == 4


def solve():
    return coinSums(200, [1, 2, 5, 10, 20, 50, 100, 200])


if __name__ == "__main__":
    runTests()
    print(solve())
