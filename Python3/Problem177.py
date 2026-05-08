import math
import time


TOLERANCE = 10 ** -9


def canonical(angles):
    pairs = (
        (angles[0], angles[1]),
        (angles[2], angles[3]),
        (angles[4], angles[5]),
        (angles[6], angles[7]),
    )
    reversed_pairs = tuple((right, left) for left, right in reversed(pairs))

    candidates = []
    for orientation in (pairs, reversed_pairs):
        for start in range(4):
            rotated = orientation[start:] + orientation[:start]
            candidates.append(tuple(angle for pair in rotated for angle in pair))

    return min(candidates)


def isIntegerAngle(angle):
    return abs(angle - round(angle)) <= TOLERANCE


def integerAngledQuadrilateralCount():
    sin_degrees = [math.sin(math.radians(angle)) for angle in range(181)]
    cos_degrees = [math.cos(math.radians(angle)) for angle in range(181)]
    seen = set()

    for total_bc in range(2, 179):
        limit = 180 - total_bc
        for b in range(1, total_bc):
            c = total_bc - b
            sin_b = sin_degrees[b]

            for a in range(1, limit):
                h = limit - a
                fixed_ratio = sin_degrees[a + b] / (
                    sin_degrees[a + total_bc] * sin_b
                )

                for d in range(1, limit):
                    e = limit - d
                    ratio = fixed_ratio * sin_degrees[total_bc + d]
                    g_angle = math.degrees(
                        math.atan2(sin_degrees[d], ratio - cos_degrees[d])
                    )

                    if not isIntegerAngle(g_angle):
                        continue

                    g = int(round(g_angle))
                    if not 1 <= g < total_bc:
                        continue

                    f = total_bc - g
                    seen.add(canonical((a, b, c, d, e, f, g, h)))

    return len(seen)


def runTests():
    assert canonical((45, 45, 45, 45, 45, 45, 45, 45)) == (
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
    )
    assert canonical((20, 60, 50, 30, 40, 30, 80, 50)) == (
        20,
        60,
        50,
        30,
        40,
        30,
        80,
        50,
    )


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = integerAngledQuadrilateralCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
