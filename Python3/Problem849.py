import time


MOD = 1_000_000_007


def F(teams, modulus=MOD):
    if teams <= 0:
        return 0
    if teams == 1:
        return 1

    maxDiff = 2 * (teams - 1)
    offset = maxDiff
    diffCount = 2 * maxDiff + 1
    maxHeight = [2 * i * (teams - i) for i in range(teams + 1)]

    dp = [[0] * diffCount for _ in range(maxHeight[1] + 1)]
    for diff in range(maxDiff + 1):
        dp[diff][diff + offset] = 1

    for step in range(1, teams):
        currentMaxHeight = maxHeight[step]
        nextMaxHeight = maxHeight[step + 1]
        nextDp = [[0] * diffCount for _ in range(nextMaxHeight + 1)]

        for height in range(currentMaxHeight + 1):
            row = dp[height]
            cumulative = 0

            base = height - offset - 4
            start = max(4, -base)
            start = min(start, diffCount)
            end = min(diffCount - 1, nextMaxHeight - base)

            for index in range(start):
                cumulative += row[index]
                if cumulative >= modulus:
                    cumulative -= modulus

            if start <= end:
                for index in range(start, end + 1):
                    cumulative += row[index]
                    if cumulative >= modulus:
                        cumulative -= modulus

                    nextHeight = base + index
                    nextIndex = index - 4
                    nextDp[nextHeight][nextIndex] = (
                        nextDp[nextHeight][nextIndex] + cumulative
                    ) % modulus

                for index in range(end + 1, diffCount):
                    cumulative += row[index]
                    if cumulative >= modulus:
                        cumulative -= modulus
            else:
                for index in range(start, diffCount):
                    cumulative += row[index]
                    if cumulative >= modulus:
                        cumulative -= modulus

            total = cumulative
            if total:
                baseHeight = height - offset
                for index in range(diffCount - 4, diffCount):
                    nextHeight = baseHeight + index
                    if 0 <= nextHeight <= nextMaxHeight:
                        nextDp[nextHeight][index] = (nextDp[nextHeight][index] + total) % modulus

        dp = nextDp

    return sum(dp[0]) % modulus


def runTests():
    assert F(2) == 3
    assert F(7) == 32_923


def solve():
    return F(100)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
