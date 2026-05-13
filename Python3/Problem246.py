import math
import time


CENTER_X = 3000
CENTER_Y = 1500
SEMI_MAJOR = 7500
SEMI_MINOR_SQUARED = 31250000
ANGLE_LIMIT_SQUARED_TANGENT = 1


def floorSqrtDiv(numerator, denominator):
    result = math.isqrt(numerator // denominator)

    while (result + 1) * (result + 1) * denominator <= numerator:
        result += 1
    while result * result * denominator > numerator:
        result -= 1

    return result


def firstOutsideEllipse(abs_y):
    a_squared = SEMI_MAJOR * SEMI_MAJOR
    b_squared = SEMI_MINOR_SQUARED

    if abs_y * abs_y > b_squared:
        return 0

    return floorSqrtDiv(a_squared * b_squared - abs_y * abs_y * a_squared, b_squared) + 1


def hasWideTangentAngle(abs_x, abs_y):
    a = float(SEMI_MAJOR)
    b = math.sqrt(float(SEMI_MINOR_SQUARED))
    alpha = abs_x / a
    beta = abs_y / b
    radius_squared = alpha * alpha + beta * beta

    if radius_squared <= 1.0:
        return False

    line_component = 1.0 / radius_squared - 1.0
    tangent_component = math.sqrt(radius_squared - 1.0) / radius_squared

    dx1 = a * (line_component * alpha - tangent_component * beta)
    dy1 = b * (line_component * beta + tangent_component * alpha)
    dx2 = a * (line_component * alpha + tangent_component * beta)
    dy2 = b * (line_component * beta - tangent_component * alpha)

    dot_product = dx1 * dx2 + dy1 * dy2
    if dot_product <= 0:
        return True

    norm_product = (dx1 * dx1 + dy1 * dy1) * (dx2 * dx2 + dy2 * dy2)
    return 2 * dot_product * dot_product < norm_product


def rowCount(abs_y):
    first_x = firstOutsideEllipse(abs_y)
    if not hasWideTangentAngle(first_x, abs_y):
        return 0

    high = max(first_x, 1)
    while hasWideTangentAngle(high, abs_y):
        high *= 2

    low = first_x
    high -= 1

    while low < high:
        middle = (low + high + 1) // 2
        if hasWideTangentAngle(middle, abs_y):
            low = middle
        else:
            high = middle - 1

    result = 2 * (low - first_x + 1)
    if first_x == 0:
        result -= 1

    return result


def latticePointsWithWideTangents():
    abs_y = math.isqrt(SEMI_MINOR_SQUARED) + 1
    while hasWideTangentAngle(0, abs_y):
        abs_y += 1

    max_abs_y = abs_y - 1
    total = rowCount(0)

    for y in range(1, max_abs_y + 1):
        total += 2 * rowCount(y)

    return total


def runTests():
    assert firstOutsideEllipse(0) == 7501
    assert rowCount(0) == 15878


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = latticePointsWithWideTangents()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
