from bisect import bisect_left, insort
from math import isqrt
import time


MOD = 1_405_695_061


def replaceOne(sortedTuple, old, new):
    values = list(sortedTuple)
    index = bisect_left(values, old)
    assert index < len(values) and values[index] == old
    values.pop(index)
    insort(values, new)
    return tuple(values)


def Mk(k, limit, modulus=None):
    if limit < 1:
        return 0

    seenNumbers = {1}
    total = 1
    if modulus is not None:
        total %= modulus

    if k - 1 > limit:
        return total if modulus is None else total % modulus

    stack = [((), 1)]
    visitedStates = {()}

    while stack:
        nonOnes, productNonOnes = stack.pop()
        ones = k - len(nonOnes)

        for value in nonOnes:
            if value <= limit and value not in seenNumbers:
                seenNumbers.add(value)
                total += value
                if modulus is not None:
                    total %= modulus

        jumpValues = set(nonOnes)
        if ones:
            jumpValues.add(1)

        for value in jumpValues:
            if value == 1:
                newValue = k * productNonOnes - 1
                if newValue <= 1 or newValue > limit:
                    continue
                newState = tuple(sorted(nonOnes + (newValue,)))
                newProduct = productNonOnes * newValue
            else:
                newValue = k * (productNonOnes // value) - value
                if newValue <= value or newValue > limit:
                    continue
                newState = replaceOne(nonOnes, value, newValue)
                newProduct = (productNonOnes // value) * newValue

            if newState not in visitedStates:
                visitedStates.add(newState)
                stack.append((newState, newProduct))

    return total if modulus is None else total % modulus


def thirdNonOneMinimum(k):
    return k**4 - 2 * k**3 + k - 1


def a2(k):
    return k * k - k - 1


def a3(k):
    return k * k * k - k * k - 2 * k + 1


def maxKMonotoneTrue(limit, start, predicate):
    if limit < start:
        return limit
    if not predicate(start):
        return start - 1

    low = start
    high = start
    while high < limit and predicate(high):
        low = high
        high = min(limit, high * 2)

    if predicate(high):
        return high

    while low + 1 < high:
        middle = (low + high) // 2
        if predicate(middle):
            low = middle
        else:
            high = middle

    return low


def maxKThreeNonOnes(limit, maxK):
    if maxK < 3:
        return maxK
    return maxKMonotoneTrue(maxK, 3, lambda k: thirdNonOneMinimum(k) <= limit)


def maxKA2(limit, maxK):
    if maxK < 1:
        return 0

    discriminant = 1 + 4 * (limit + 1)
    root = min((1 + isqrt(discriminant)) // 2, maxK)
    while root > 0 and a2(root) > limit:
        root -= 1
    return root


def maxKA3(limit, maxK):
    if maxK < 3:
        return maxK
    if a3(3) > limit:
        return 2
    return maxKMonotoneTrue(maxK, 3, lambda k: a3(k) <= limit)


def sum1(n):
    return n * (n + 1) // 2


def sum2(n):
    return n * (n + 1) * (2 * n + 1) // 6


def sum3(n):
    value = n * (n + 1) // 2
    return value * value


def rangeSum(function, left, right):
    if left > right:
        return 0
    return function(right) - function(left - 1)


def SMod(maxK, limit, modulus=MOD):
    if maxK < 3 or limit < 1:
        return 0

    effectiveK = min(maxK, limit + 1)
    total = 0
    cutoff = min(effectiveK, maxKThreeNonOnes(limit, effectiveK))

    for k in range(3, cutoff + 1):
        total = (total + Mk(k, limit, modulus)) % modulus

    start = cutoff + 1
    if start <= effectiveK:
        k3 = min(effectiveK, maxKA3(limit, effectiveK))
        k2 = min(effectiveK, maxKA2(limit, effectiveK))

        left, right = start, k3
        if left <= right:
            total += rangeSum(sum3, left, right) - 2 * rangeSum(sum1, left, right)
            total %= modulus

        left, right = max(start, k3 + 1), k2
        if left <= right:
            total += rangeSum(sum2, left, right) - (right - left + 1)
            total %= modulus

        left, right = max(start, k2 + 1), effectiveK
        if left <= right:
            total += rangeSum(sum1, left, right)
            total %= modulus

    if maxK > effectiveK:
        total = (total + (maxK - effectiveK)) % modulus

    return total % modulus


def SExactSmall(maxK, limit):
    return sum(Mk(k, limit) for k in range(3, maxK + 1))


def runTests():
    assert Mk(3, 10**3) == 2797
    assert Mk(8, 10**8) == 131_493_335
    assert SExactSmall(4, 10**2) == 229
    assert SExactSmall(10, 10**8) == 2_383_369_980


def solve():
    return SMod(10**18, 10**18)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
