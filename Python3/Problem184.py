import math
import time


def choose2(number):
    if number < 2:
        return 0
    return number * (number - 1) // 2


def choose3(number):
    if number < 3:
        return 0
    return number * (number - 1) * (number - 2) // 6


def rayCounts(radius):
    counts = {}

    for x in range(-radius + 1, radius):
        for y in range(-radius + 1, radius):
            if (x == 0 and y == 0) or x * x + y * y >= radius * radius:
                continue

            divisor = math.gcd(abs(x), abs(y))
            direction = (x // divisor, y // divisor)
            counts[direction] = counts.get(direction, 0) + 1

    return counts


def trianglesContainingOrigin(radius):
    counts = rayCounts(radius)
    directions = sorted(
        counts, key=lambda direction: math.atan2(direction[1], direction[0]) % (2 * math.pi)
    )
    angles = [
        math.atan2(direction[1], direction[0]) % (2 * math.pi)
        for direction in directions
    ]
    weights = [counts[direction] for direction in directions]
    direction_count = len(directions)
    point_count = sum(weights)

    extended_angles = angles + [angle + 2 * math.pi for angle in angles]
    extended_weights = weights * 2
    prefix_weights = [0]
    for weight in extended_weights:
        prefix_weights.append(prefix_weights[-1] + weight)

    bad_open_semicircle = 0
    end = 0
    for start in range(direction_count):
        if end < start + 1:
            end = start + 1
        while (
            end < start + direction_count
            and extended_angles[end] - extended_angles[start] < math.pi - 10 ** -12
        ):
            end += 1

        window_points = prefix_weights[end] - prefix_weights[start]
        bad_open_semicircle += choose3(window_points) - choose3(
            window_points - weights[start]
        )

    bad_opposite = 0
    seen = set()
    for direction, weight in counts.items():
        if direction in seen:
            continue

        opposite = (-direction[0], -direction[1])
        opposite_weight = counts.get(opposite, 0)
        seen.add(direction)
        seen.add(opposite)

        bad_opposite += (
            weight * opposite_weight * (point_count - weight - opposite_weight)
            + choose2(weight) * opposite_weight
            + weight * choose2(opposite_weight)
        )

    return choose3(point_count) - bad_open_semicircle - bad_opposite


def runTests():
    assert trianglesContainingOrigin(2) == 8
    assert trianglesContainingOrigin(3) == 360


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = trianglesContainingOrigin(105)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
