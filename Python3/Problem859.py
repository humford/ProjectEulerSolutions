import time


def pileValues(limit):
    values = [0] * (limit + 1)

    for n in range(1, limit + 1):
        if n % 2:
            option = 2 * values[n // 2]
            values[n] = 0 if option < 0 else option + 1
        else:
            option = 2 * values[n // 2 - 1]
            values[n] = 0 if option > 0 else option - 1

    return values


def C(cookies):
    values = pileValues(cookies)
    minValue = -(cookies // 2)
    maxValue = cookies
    width = maxValue - minValue + 1
    offset = -minValue

    dp = [[0] * width for _ in range(cookies + 1)]
    dp[0][offset] = 1

    for size in range(1, cookies + 1):
        delta = values[size]

        if delta >= 0:
            for totalCookies in range(size, cookies + 1):
                source = dp[totalCookies - size]
                target = dp[totalCookies]
                for valueIndex in range(delta, width):
                    target[valueIndex] += source[valueIndex - delta]
        else:
            shift = -delta
            for totalCookies in range(size, cookies + 1):
                source = dp[totalCookies - size]
                target = dp[totalCookies]
                for valueIndex in range(0, width - shift):
                    target[valueIndex] += source[valueIndex + shift]

    return sum(dp[cookies][:offset + 1])


def runTests():
    assert C(5) == 2
    assert C(16) == 64


def solve():
    return C(300)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
