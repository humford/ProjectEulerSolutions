import math
import time


SIDE = 1600.0
A = (200.0, 200.0)
B = (1400.0, 1400.0)


def heightAndGradient(x, y):
    p = 5000.0 - 0.005 * (x * x + y * y + x * y) + 12.5 * (x + y)
    q = 0.000001 * (x * x + y * y) - 0.0015 * (x + y) + 0.7
    exponential = math.exp(-abs(q))
    height = p * exponential

    px = 12.5 - 0.01 * x - 0.005 * y
    py = 12.5 - 0.01 * y - 0.005 * x
    qx = 0.000002 * x - 0.0015
    qy = 0.000002 * y - 0.0015
    sign = 1.0 if q >= 0.0 else -1.0

    return (
        height,
        exponential * (px - p * sign * qx),
        exponential * (py - p * sign * qy),
    )


def height(x, y):
    return heightAndGradient(x, y)[0]


def goldenSectionMaximum(function, low, high):
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    left = high - ratio * (high - low)
    right = low + ratio * (high - low)
    left_value = function(left)
    right_value = function(right)

    for _ in range(200):
        if left_value < right_value:
            low = left
            left = right
            left_value = right_value
            right = low + ratio * (high - low)
            right_value = function(right)
        else:
            high = right
            right = left
            right_value = left_value
            left = high - ratio * (high - low)
            left_value = function(left)

    point = (low + high) / 2.0
    return point, function(point)


def minimumFlightElevation():
    best_y = max(range(1601), key=lambda y: height(0.0, float(y)))
    return goldenSectionMaximum(
        lambda y: height(0.0, y),
        max(0.0, best_y - 5.0),
        min(SIDE, best_y + 5.0),
    )


def tangentEquations(origin, flight_height, x, y):
    ox, oy = origin
    terrain_height, hx, hy = heightAndGradient(x, y)
    return terrain_height - flight_height, hx * (ox - x) + hy * (oy - y)


def tangentPoint(origin, flight_height, x, y):
    for _ in range(100):
        first, second = tangentEquations(origin, flight_height, x, y)
        if abs(first) < 1e-10 and abs(second) < 1e-8:
            return x, y

        dx = 1e-6 * max(1.0, abs(x))
        dy = 1e-6 * max(1.0, abs(y))
        fpx, spx = tangentEquations(origin, flight_height, x + dx, y)
        fmx, smx = tangentEquations(origin, flight_height, x - dx, y)
        fpy, spy = tangentEquations(origin, flight_height, x, y + dy)
        fmy, smy = tangentEquations(origin, flight_height, x, y - dy)

        dfirst_dx = (fpx - fmx) / (2.0 * dx)
        dsecond_dx = (spx - smx) / (2.0 * dx)
        dfirst_dy = (fpy - fmy) / (2.0 * dy)
        dsecond_dy = (spy - smy) / (2.0 * dy)
        determinant = dfirst_dx * dsecond_dy - dfirst_dy * dsecond_dx
        if abs(determinant) < 1e-18:
            break

        step_x = (-first * dsecond_dy + second * dfirst_dy) / determinant
        step_y = (-dfirst_dx * second + dsecond_dx * first) / determinant
        old_error = abs(first) + abs(second)
        scale = 1.0

        for _ in range(25):
            next_x = x + scale * step_x
            next_y = y + scale * step_y
            if 0.0 <= next_x <= SIDE and 0.0 <= next_y <= SIDE:
                next_first, next_second = tangentEquations(
                    origin, flight_height, next_x, next_y
                )
                if abs(next_first) + abs(next_second) < old_error:
                    x, y = next_x, next_y
                    break
            scale *= 0.5

    return x, y


def projectToContour(x, y, flight_height):
    for _ in range(3):
        terrain_height, hx, hy = heightAndGradient(x, y)
        error = terrain_height - flight_height
        squared_gradient = hx * hx + hy * hy
        if squared_gradient == 0:
            break
        x -= error * hx / squared_gradient
        y -= error * hy / squared_gradient

    return x, y


def contourTangent(x, y, direction):
    _, hx, hy = heightAndGradient(x, y)
    length = math.hypot(hx, hy)
    return -direction * hy / length, direction * hx / length


def contourStep(x, y, flight_height, step, direction):
    k1x, k1y = contourTangent(x, y, direction)
    k2x, k2y = contourTangent(x + 0.5 * step * k1x, y + 0.5 * step * k1y, direction)
    k3x, k3y = contourTangent(x + 0.5 * step * k2x, y + 0.5 * step * k2y, direction)
    k4x, k4y = contourTangent(x + step * k3x, y + step * k3y, direction)

    return projectToContour(
        x + step * (k1x + 2 * k2x + 2 * k3x + k4x) / 6.0,
        y + step * (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0,
        flight_height,
    )


def contourArcLength(start, target, flight_height, direction):
    x, y = projectToContour(start[0], start[1], flight_height)
    target_x, target_y = target
    total = 0.0
    step = 0.1

    for _ in range(2000000):
        distance = math.hypot(x - target_x, y - target_y)
        if distance < 1e-10:
            return total

        step = min(step, max(1e-10, 0.5 * distance))
        next_x, next_y = contourStep(x, y, flight_height, step, direction)
        next_distance = math.hypot(next_x - target_x, next_y - target_y)

        if distance < 1.0 and next_distance > distance:
            step *= 0.5
            if step < 1e-12:
                return None
            continue

        x, y = next_x, next_y
        total += step
        if total > 20000.0:
            return None

    return None


def shortestMountainPath():
    _, flight_height = minimumFlightElevation()
    tangent_seeds_a = ((50.0, 625.0), (625.0, 50.0))
    tangent_seeds_b = ((875.0, 1535.0), (1535.0, 875.0))
    tangents_a = [tangentPoint(A, flight_height, x, y) for x, y in tangent_seeds_a]
    tangents_b = [tangentPoint(B, flight_height, x, y) for x, y in tangent_seeds_b]
    best = float("inf")

    for first in tangents_a:
        for second in tangents_b:
            lengths = [
                contourArcLength(first, second, flight_height, direction)
                for direction in (-1.0, 1.0)
            ]
            arc_lengths = [length for length in lengths if length is not None]
            if not arc_lengths:
                continue

            total = (
                math.hypot(first[0] - A[0], first[1] - A[1])
                + min(arc_lengths)
                + math.hypot(second[0] - B[0], second[1] - B[1])
            )
            best = min(best, total)

    return format(best, ".3f")


def runTests():
    pass_y, flight_height = minimumFlightElevation()
    assert abs(pass_y - 895.4834083597696) < 1e-6
    assert abs(flight_height - 10396.462193284104) < 1e-6


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = shortestMountainPath()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
