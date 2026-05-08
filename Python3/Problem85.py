import time


def rectangleCount(width, height):
    return width * (width + 1) * height * (height + 1) // 4


def nearestRectangleArea(target):
    best_difference = target
    best_area = None

    width = 1
    while rectangleCount(width, 1) - target <= best_difference:
        for height in range(1, width + 1):
            count = rectangleCount(width, height)
            difference = abs(count - target)
            if difference < best_difference:
                best_difference = difference
                best_area = width * height
            if count > target and difference > best_difference:
                break
        width += 1

    return best_area


def runTests():
    assert rectangleCount(3, 2) == 18


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nearestRectangleArea(2000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
