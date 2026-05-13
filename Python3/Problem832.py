import time


MOD = 1_000_000_007


def mex(sortedValues):
    expected = 0
    for value in sortedValues:
        if value == expected:
            expected += 1
        elif value > expected:
            break
    return expected


def bruteM(n):
    paper = [0]

    for _ in range(n):
        a = mex(paper)
        paper.append(a)
        paper.sort()

        b = mex(paper)
        paperSet = set(paper)
        while b in paperSet or (a ^ b) in paperSet:
            b += 1

        paper.append(b)
        paper.append(a ^ b)
        paper.sort()

    return sum(paper)


def intervalSum(start, length):
    end = start + length - 1
    return (start + end) * length // 2


def blockSum(a, b, c, length):
    return (
        intervalSum(a, length)
        + intervalSum(b, length)
        + intervalSum(c, length)
    )


def mexSequenceSum(n, a=1, b=2, c=3, powerIndex=0):
    if n <= 0:
        return 0

    power = 4**powerIndex
    if power < n:
        return (
            mexSequenceSum(power, a, b, c, powerIndex)
            + mexSequenceSum(n - power, 4 * a, 4 * b, 4 * c, powerIndex + 1)
        ) % MOD

    if power == n:
        return blockSum(a, b, c, power) % MOD

    subPower = power // 4
    total = 0
    total += mexSequenceSum(min(n, subPower), a, b, c, powerIndex - 1)
    total += mexSequenceSum(
        min(n - subPower, subPower),
        a + subPower,
        b + 2 * subPower,
        c + 3 * subPower,
        powerIndex - 1,
    )
    total += mexSequenceSum(
        min(n - 2 * subPower, subPower),
        a + 2 * subPower,
        b + 3 * subPower,
        c + subPower,
        powerIndex - 1,
    )
    total += mexSequenceSum(
        min(n - 3 * subPower, subPower),
        a + 3 * subPower,
        b + subPower,
        c + 2 * subPower,
        powerIndex - 1,
    )

    return total % MOD


def solve(n):
    return mexSequenceSum(n)


def runTests():
    assert bruteM(10) == 642
    assert solve(10) == 642
    assert solve(1000) == 5432148


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve(10**18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
