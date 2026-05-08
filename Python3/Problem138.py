import time


def specialTriangleLegs(count):
    legs = [17, 305]
    while len(legs) < count:
        legs.append(18 * legs[-1] - legs[-2])
    return legs[:count]


def runTests():
    assert specialTriangleLegs(4) == [17, 305, 5473, 98209]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sum(specialTriangleLegs(12))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
