import time


SIZE = 30
MODULUS = 10**8


def boundaryPoints(size):
    points = []

    for x in range(size + 1):
        points.append((x, 0))
    for y in range(1, size + 1):
        points.append((size, y))
    for x in range(size - 1, -1, -1):
        points.append((x, size))
    for y in range(size - 1, 0, -1):
        points.append((0, y))

    return points


def sideMask(point, size):
    x, y = point
    result = 0

    if y == 0:
        result |= 1
    if x == size:
        result |= 2
    if y == size:
        result |= 4
    if x == 0:
        result |= 8

    return result


def cuttingCount(size, modulus):
    points = boundaryPoints(size)
    point_count = len(points)
    masks = [sideMask(point, size) for point in points]
    type_map = {1: 0, 2: 1, 4: 2, 8: 3, 3: 4, 6: 5, 12: 6, 9: 7}
    types = [type_map[mask] for mask in masks]
    masks_by_type = [0] * 8

    for mask, point_type in type_map.items():
        masks_by_type[point_type] = mask

    compatible = [0] * 8
    for point_type in range(8):
        for other_type in range(8):
            if masks_by_type[point_type] & masks_by_type[other_type]:
                compatible[point_type] |= 1 << other_type

    allowed_cut = [[False] * point_count for _ in range(point_count)]
    for start in range(point_count):
        for end in range(start + 2, point_count):
            allowed_cut[start][end] = not (masks[start] & masks[end])

    dp = [[0] * point_count for _ in range(point_count)]
    for index in range(point_count - 1):
        dp[index][index + 1] = 1

    all_types = (1 << 8) - 1

    for length in range(2, point_count):
        for start in range(point_count - length):
            end = start + length
            memo = {}

            def paths(position, allowed_types):
                key = (position, allowed_types)
                if key in memo:
                    return memo[key]

                result = 0
                for next_position in range(position + 1, end + 1):
                    if position == start and next_position == end:
                        continue
                    if not (allowed_types >> types[next_position]) & 1:
                        continue
                    if next_position != position + 1 and not allowed_cut[position][
                        next_position
                    ]:
                        continue
                    if (
                        position != start
                        and next_position != end
                        and (masks[next_position] & masks[start]) == 0
                    ):
                        continue
                    if (
                        next_position != end
                        and position != start
                        and (masks[position] & masks[end]) == 0
                    ):
                        continue

                    weight = dp[position][next_position]
                    if weight == 0:
                        continue

                    if next_position == end:
                        result += weight
                    else:
                        next_allowed_types = (
                            allowed_types
                            if position == start
                            else allowed_types & compatible[types[position]]
                        )
                        result += weight * paths(next_position, next_allowed_types)

                memo[key] = result % modulus
                return memo[key]

            dp[start][end] = paths(start, all_types)

    return dp[0][point_count - 1] % modulus


def runTests():
    assert cuttingCount(1, MODULUS) == 2
    assert cuttingCount(2, MODULUS) == 30


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = cuttingCount(SIZE, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
