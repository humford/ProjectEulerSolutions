import time


MOD = 1_000_000_007


def g(m, n):
    return (m ^ n) + (m | n) + (m & n)


def bruteG(limit):
    total = 0
    for n in range(limit + 1):
        for k in range(n + 1):
            total += g(k, n - k)
    return total


def brutePairCount(limit, fixedZeroBit=None):
    count = 0
    for a in range(limit + 1):
        for b in range(limit - a + 1):
            if fixedZeroBit is None:
                count += 1
            elif ((a >> fixedZeroBit) & 1) == 0 and ((b >> fixedZeroBit) & 1) == 0:
                count += 1
    return count


def countPairsWithSumAtMost(limit, fixedZeroBit=None):
    if limit < 0:
        return 0

    bitCount = max(1, limit.bit_length())
    # State is dp[carry_into_higher_bit][already_less_than_limit].
    dp = [[0, 0], [0, 0]]
    dp[0][0] = 1

    for position in range(bitCount - 1, -1, -1):
        limitBit = (limit >> position) & 1
        nextDp = [[0, 0], [0, 0]]
        for carryNext in range(2):
            for less in range(2):
                ways = dp[carryNext][less]
                if ways == 0:
                    continue

                for carryCurrent in range(2):
                    for aBit in range(2):
                        for bBit in range(2):
                            if (
                                fixedZeroBit is not None
                                and position == fixedZeroBit
                                and (aBit or bBit)
                            ):
                                continue

                            total = aBit + bBit + carryCurrent
                            if total >> 1 != carryNext:
                                continue

                            sumBit = total & 1
                            if less == 0 and sumBit > limitBit:
                                continue

                            nextLess = less or (sumBit < limitBit)
                            nextDp[carryCurrent][nextLess] = (
                                nextDp[carryCurrent][nextLess] + ways
                            ) % MOD

        dp = nextDp

    return (dp[0][0] + dp[0][1]) % MOD


def G(limit):
    inverseTwo = (MOD + 1) // 2
    totalPairs = (limit + 1) % MOD
    totalPairs = totalPairs * ((limit + 2) % MOD) % MOD
    totalPairs = totalPairs * inverseTwo % MOD

    totalOr = 0
    powerOfTwo = 1
    for bit in range(max(1, limit.bit_length())):
        bothZero = countPairsWithSumAtMost(limit, bit)
        bitOne = (totalPairs - bothZero) % MOD
        totalOr = (totalOr + powerOfTwo * bitOne) % MOD
        powerOfTwo = powerOfTwo * 2 % MOD

    return 2 * totalOr % MOD


def runTests():
    for m in range(16):
        for n in range(16):
            assert g(m, n) == 2 * (m | n)

    for limit in range(1, 32):
        assert countPairsWithSumAtMost(limit) == brutePairCount(limit)
        for bit in range(limit.bit_length()):
            assert countPairsWithSumAtMost(limit, bit) == brutePairCount(limit, bit)

    assert G(10) == 754
    assert G(10 ** 2) == 583_766
    assert G(50) == bruteG(50) % MOD


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = G(10 ** 18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
