from math import isqrt
import time


TARGET_N = 10**16
MODULUS = 10**9


def floorDivSqrt(numerator, denominator):
    if numerator <= 0:
        return 0

    square = numerator * numerator
    quotient = isqrt(square // denominator)

    while (quotient + 1) * (quotient + 1) * denominator <= square:
        quotient += 1
    while quotient * quotient * denominator > square:
        quotient -= 1

    return quotient


def ceilDivSqrt(numerator, denominator):
    if numerator <= 0:
        return 0
    return floorDivSqrt(numerator, denominator) + 1


def initialPrefixSum(limit, coins):
    terms = min(limit, 2 * coins)
    if terms <= 0:
        return 0

    pairs = terms // 2
    total = 2 * (pairs * coins - pairs * (pairs - 1) // 2)
    if terms % 2 == 1:
        total += coins - pairs

    return total


def nextReset(previousReset, coins, denominator):
    if coins == 0:
        return 2 * previousReset

    threshold = 1
    while threshold <= coins:
        quotient = coins // threshold
        candidate = 2 * previousReset - 2 * quotient
        distance = candidate - previousReset

        if distance > 0:
            bribeCost = ceilDivSqrt(distance, denominator)
            if coins // bribeCost == quotient:
                return candidate

        threshold = coins // quotient + 1

    return 2 * previousReset


def T(limit, coins, denominator):
    if limit <= 0:
        return 0

    firstZeroReset = 2 * coins + 2
    if limit <= firstZeroReset:
        return initialPrefixSum(limit, coins)

    total = initialPrefixSum(firstZeroReset, coins)
    previousReset = firstZeroReset
    resetCoins = 0

    while previousReset < limit:
        reset = nextReset(previousReset, coins, denominator)

        if reset > limit:
            distance = limit - previousReset + 1
            total += (distance - 1) * resetCoins + (distance - 1) * distance // 2
            break

        distance = reset - previousReset
        if distance > 1:
            total += (distance - 1) * resetCoins + (distance - 1) * distance // 2

        requiredVotes = (reset + 1) // 2
        freeVotes = distance
        bribesNeeded = max(requiredVotes - freeVotes, 0)
        resetCoins = coins - bribesNeeded * ceilDivSqrt(distance, denominator)
        total += resetCoins
        previousReset = reset

    return total


def bruteT(limit, coins, denominator):
    state = [(coins, 0)]
    total = coins

    for pirateCount in range(2, limit + 1):
        bribeCosts = []
        for outcome in state:
            if outcome is None:
                bribeCosts.append(0)
            else:
                pirateCoins, planks = outcome
                bribeCosts.append(
                    pirateCoins + ceilDivSqrt(planks + 1, denominator)
                )

        bribesNeeded = (pirateCount + 1) // 2 - 1
        bribed = set(
            sorted(range(pirateCount - 1), key=lambda i: (bribeCosts[i], i))[
                :bribesNeeded
            ]
        )
        totalBribeCost = sum(bribeCosts[i] for i in bribed)

        if totalBribeCost <= coins:
            state = [(coins - totalBribeCost, 0)] + [
                (bribeCosts[i] if i in bribed else 0, 0)
                for i in range(pirateCount - 1)
            ]
        else:
            state = [None] + [
                None if outcome is None else (outcome[0], outcome[1] + 1)
                for outcome in state
            ]

        for outcome in state:
            if outcome is not None:
                total += outcome[0] + outcome[1]
                break

    return total


def solve():
    total = 0
    for exponent in range(1, 7):
        coins = 10**exponent + 1
        total += T(TARGET_N, coins, coins)
    return total % MODULUS


def runTests():
    assert T(30, 3, 3) == 190
    assert T(50, 3, 31) == 385
    assert T(10**3, 101, 101) == 142_427

    for coins, denominator in ((1, 3), (2, 3), (3, 3), (3, 31), (5, 7)):
        for limit in range(1, 30):
            assert T(limit, coins, denominator) == bruteT(limit, coins, denominator)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer).zfill(9) + " in " + str(elapsed) + " seconds.")
