import math
import time


def streak(n):
    k = 1
    while (n + k) % (k + 1) == 0:
        k += 1
    return k


def lcmUpTo(limit):
    value = 1
    for factor in range(2, limit + 1):
        value = value * factor // math.gcd(value, factor)
    return value


def streakCount(s, limit):
    currentLcm = lcmUpTo(s)
    nextLcm = currentLcm * (s + 1) // math.gcd(currentLcm, s + 1)
    return (limit - 2) // currentLcm - (limit - 2) // nextLcm


def streakPowerSum():
    return sum(streakCount(index, 4 ** index) for index in range(1, 32))


def runTests():
    assert streak(13) == 4
    assert streak(120) == 1
    assert streakCount(3, 14) == 1
    assert streakCount(6, 10 ** 6) == 14_286


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = streakPowerSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
