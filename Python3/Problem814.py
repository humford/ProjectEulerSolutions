import time


MOD = 998_244_353
LEFT = 0
RIGHT = 1
OPPOSITE = 2


def swapMask(mask):
    return ((mask & 1) << 1) | (mask >> 1)


def transitionGroups(finalColumn=False):
    groups = []

    for incoming in range(4):
        grouped = {}
        topIncoming = incoming & 1
        bottomIncoming = (incoming >> 1) & 1

        for topChoice in (LEFT, RIGHT, OPPOSITE):
            for bottomChoice in (LEFT, RIGHT, OPPOSITE):
                outMask = 0
                if topChoice == RIGHT:
                    outMask |= 1
                if bottomChoice == RIGHT:
                    outMask |= 2
                if finalColumn:
                    outMask = swapMask(outMask)

                pairs = 0
                if topIncoming and topChoice == LEFT:
                    pairs += 1
                if bottomIncoming and bottomChoice == LEFT:
                    pairs += 1
                if topChoice == OPPOSITE and bottomChoice == OPPOSITE:
                    pairs += 1

                key = (outMask, pairs)
                grouped[key] = grouped.get(key, 0) + 1

        groups.append([(outMask, pairs, count) for (outMask, pairs), count in grouped.items()])

    return groups


NORMAL_GROUPS = transitionGroups(False)
FINAL_GROUPS = transitionGroups(True)


def addMod(value, addend):
    value += addend
    while value >= MOD:
        value -= MOD
    return value


def step(dp, groups, target):
    nextDp = [[0] * (target + 1) for _ in range(4)]

    for incoming in range(4):
        source = dp[incoming]
        for outgoing, delta, count in groups[incoming]:
            destination = nextDp[outgoing]
            limit = target - delta + 1
            if count == 1:
                for k in range(limit):
                    destination[k + delta] = addMod(destination[k + delta], source[k])
            elif count == 2:
                for k in range(limit):
                    addend = source[k] * 2
                    if addend >= MOD:
                        addend -= MOD
                    destination[k + delta] = addMod(destination[k + delta], addend)
            else:
                for k in range(limit):
                    addend = source[k] * 3
                    while addend >= MOD:
                        addend -= MOD
                    destination[k + delta] = addMod(destination[k + delta], addend)

    return nextDp


def S(n, modulus=MOD):
    if modulus != MOD:
        raise ValueError("This implementation is specialized for the Project Euler modulus")

    targetPairs = n
    columns = 2 * n
    total = 0

    for initialIncoming in range(4):
        dp = [[0] * (targetPairs + 1) for _ in range(4)]
        dp[initialIncoming][0] = 1

        for _ in range(columns - 1):
            dp = step(dp, NORMAL_GROUPS, targetPairs)

        dp = step(dp, FINAL_GROUPS, targetPairs)
        total = (total + dp[initialIncoming][targetPairs]) % MOD

    return total


def runTests():
    assert S(1) == 48
    assert S(10) == 420_121_075


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = S(10 ** 3)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
