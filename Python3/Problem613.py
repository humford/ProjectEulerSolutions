import math
import time


def visualAngle(point, endpoint_a, endpoint_b):
    ax, ay = endpoint_a[0] - point[0], endpoint_a[1] - point[1]
    bx, by = endpoint_b[0] - point[0], endpoint_b[1] - point[1]
    return math.atan2(abs(ax * by - ay * bx), ax * bx + ay * by)


def adaptiveSimpson(function, left, right, tolerance, maxDepth=24):
    middle = (left + right) / 2
    leftValue = function(left)
    middleValue = function(middle)
    rightValue = function(right)
    estimate = (right - left) * (leftValue + 4 * middleValue + rightValue) / 6

    def refine(left, middle, right, leftValue, middleValue, rightValue, estimate, tolerance, depth):
        leftMiddle = (left + middle) / 2
        rightMiddle = (middle + right) / 2
        leftMiddleValue = function(leftMiddle)
        rightMiddleValue = function(rightMiddle)

        leftEstimate = (
            (middle - left)
            * (leftValue + 4 * leftMiddleValue + middleValue)
            / 6
        )
        rightEstimate = (
            (right - middle)
            * (middleValue + 4 * rightMiddleValue + rightValue)
            / 6
        )
        refined = leftEstimate + rightEstimate

        if depth == 0 or abs(refined - estimate) <= 15 * tolerance:
            return refined + (refined - estimate) / 15

        return refine(
            left,
            leftMiddle,
            middle,
            leftValue,
            leftMiddleValue,
            middleValue,
            leftEstimate,
            tolerance / 2,
            depth - 1,
        ) + refine(
            middle,
            rightMiddle,
            right,
            middleValue,
            rightMiddleValue,
            rightValue,
            rightEstimate,
            tolerance / 2,
            depth - 1,
        )

    return refine(
        left,
        middle,
        right,
        leftValue,
        middleValue,
        rightValue,
        estimate,
        tolerance,
        maxDepth,
    )


def hypotenuseExitProbability(leg_a, leg_b):
    width = float(leg_a)
    height = float(leg_b)
    area = width * height / 2

    def angleAtPoint(x, y):
        return visualAngle((x, y), (width, 0.0), (0.0, height))

    def verticalIntegral(x):
        top = height * (1 - x / width)
        if top <= 0:
            return 0.0
        return adaptiveSimpson(lambda y: angleAtPoint(x, y), 0.0, top, 1e-11)

    integral = adaptiveSimpson(verticalIntegral, 0.0, width, 1e-9)
    return integral / (area * 2 * math.pi)


def longestSideExitProbability(a, b, c):
    sides = sorted((a, b, c))
    if sides[0] * sides[0] + sides[1] * sides[1] != sides[2] * sides[2]:
        raise ValueError("expected a right triangle")
    return "{:.10f}".format(hypotenuseExitProbability(sides[0], sides[1]))


def runTests():
    assert round(visualAngle((0, 0), (1, 0), (0, 1)), 12) == round(math.pi / 2, 12)
    assert longestSideExitProbability(30, 40, 50) == "0.3916721504"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = longestSideExitProbability(30, 40, 50)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
