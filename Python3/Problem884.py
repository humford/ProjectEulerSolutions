import time


TARGET_N = 10**17


def integerCubeRoot(n):
    low = 0
    high = 1
    while high**3 <= n:
        high *= 2

    while low + 1 < high:
        mid = (low + high) // 2
        if mid**3 <= n:
            low = mid
        else:
            high = mid

    return low


def D(n):
    steps = 0

    while n:
        cubeRoot = integerCubeRoot(n)
        n -= cubeRoot**3
        steps += 1

    return steps


def sumWithPrefix(limit, prefix):
    total = 0

    while limit > 1:
        cubeRoot = integerCubeRoot(limit - 1)
        remainder = limit - cubeRoot**3
        total += prefix[cubeRoot - 1] + remainder
        limit = remainder

    return total


def buildIntervalPrefix(maxCubeRoot):
    prefix = [0]

    for cubeRoot in range(1, maxCubeRoot + 1):
        intervalLength = 3 * cubeRoot * cubeRoot + 3 * cubeRoot + 1
        contribution = intervalLength + sumWithPrefix(intervalLength, prefix)
        prefix.append(prefix[-1] + contribution)

    return prefix


def S(limit):
    prefix = buildIntervalPrefix(integerCubeRoot(limit - 1))
    return sumWithPrefix(limit, prefix)


def solve():
    return S(TARGET_N)


def runTests():
    assert D(100) == 4
    assert S(100) == 512
    assert S(1000) == 6432
    assert solve() == 1105985795684653500


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
