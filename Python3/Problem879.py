from math import gcd
import time


def intermediateMasks(width, height):
    points = [
        (x, y)
        for y in range(height)
        for x in range(width)
    ]
    pointIndex = {point: index for index, point in enumerate(points)}
    pointCount = len(points)
    masks = [[0] * pointCount for _ in range(pointCount)]

    for start, (x1, y1) in enumerate(points):
        for end, (x2, y2) in enumerate(points):
            dx = x2 - x1
            dy = y2 - y1
            steps = gcd(abs(dx), abs(dy))
            if steps <= 1:
                continue

            stepX = dx // steps
            stepY = dy // steps
            mask = 0
            for k in range(1, steps):
                point = (x1 + stepX * k, y1 + stepY * k)
                mask |= 1 << pointIndex[point]
            masks[start][end] = mask

    return masks


def countPasswords(width, height):
    pointCount = width * height
    fullMask = (1 << pointCount) - 1
    required = intermediateMasks(width, height)
    counts = [[0] * pointCount for _ in range(1 << pointCount)]

    for point in range(pointCount):
        counts[1 << point][point] = 1

    total = 0
    for mask in range(1 << pointCount):
        available = fullMask ^ mask

        for last, count in enumerate(counts[mask]):
            if not count:
                continue

            candidates = available
            while candidates:
                bit = candidates & -candidates
                nextPoint = bit.bit_length() - 1
                candidates ^= bit

                needed = required[last][nextPoint]
                if needed & mask != needed:
                    continue

                counts[mask | bit][nextPoint] += count
                total += count

    return total


def solve():
    return countPasswords(4, 4)


def runTests():
    assert countPasswords(1, 2) == 2
    assert countPasswords(2, 2) == 60
    assert countPasswords(3, 3) == 389488
    assert solve() == 4350069824940


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
