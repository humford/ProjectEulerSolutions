import time
from bisect import bisect_right


def stationCount(modulus):
    stations = []
    seen = set()
    x = y = 1 % modulus

    for _ in range(2 * modulus + 1):
        station = (x, y)

        if station in seen:
            break

        seen.add(station)
        stations.append(station)
        x = (2 * x) % modulus
        y = (3 * y) % modulus

    stations.sort()
    tails = []

    for _, y in stations:
        index = bisect_right(tails, y)

        if index == len(tails):
            tails.append(y)
        else:
            tails[index] = y

    return len(tails)


def uphillPathSum():
    return sum(stationCount(k**5) for k in range(1, 31))


def runTests():
    assert stationCount(22) == 5
    assert stationCount(123) == 14
    assert stationCount(10_000) == 48


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = uphillPathSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
