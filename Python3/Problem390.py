import time


LIMIT = 10**10


def generatedTriangles(limit):
    seen = set()
    queue = []
    coordinate = 1

    while True:
        area = coordinate * (8 * coordinate * coordinate + 1)
        if area > limit:
            break

        other = 4 * coordinate * coordinate
        triangle = (min(coordinate, other), max(coordinate, other), area)
        seen.add(triangle)
        queue.append(triangle)
        coordinate += 1

    index = 0

    while index < len(queue):
        first, second, area = queue[index]
        index += 1

        for fixed, other in ((first, second), (second, first)):
            d = 4 * fixed * fixed + 1
            unitA = 8 * fixed * fixed + 1
            unitB = 4 * fixed

            for sign in (1, -1):
                nextOther = unitA * other + sign * unitB * area
                nextArea = unitA * area + sign * unitB * d * other
                nextOther = abs(nextOther)
                nextArea = abs(nextArea)

                if nextOther == 0 or nextArea > limit:
                    continue

                triangle = (
                    min(fixed, nextOther),
                    max(fixed, nextOther),
                    nextArea,
                )

                if triangle not in seen:
                    seen.add(triangle)
                    queue.append(triangle)

    return seen


def areaSum(limit=LIMIT):
    return sum(area for _, _, area in generatedTriangles(limit))


def runTests():
    assert (1, 4, 9) in generatedTriangles(10)
    assert areaSum(1_000) == 1092
    assert areaSum(1_000_000) == 18018206


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = areaSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
