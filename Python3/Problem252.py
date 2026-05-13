import collections
import math
import time


POINT_COUNT = 500


def generatePoints(count):
    state = 290797
    values = []

    for _ in range(2 * count):
        state = (state * state) % 50515093
        values.append(state % 2000 - 1000)

    return [(values[2 * i], values[2 * i + 1]) for i in range(count)]


def buildLeftBitsets(points):
    count = len(points)
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    left = [[0] * count for _ in range(count)]

    for origin in range(count):
        origin_x = xs[origin]
        origin_y = ys[origin]
        order = [point for point in range(count) if point != origin]
        order.sort(
            key=lambda point: (
                math.atan2(ys[point] - origin_y, xs[point] - origin_x),
                (xs[point] - origin_x) ** 2 + (ys[point] - origin_y) ** 2,
            )
        )

        extended = order + order
        end = 1
        window = 0

        for start in range(count - 1):
            if end < start + 1:
                end = start + 1
                window = 0

            point = extended[start]
            dx = xs[point] - origin_x
            dy = ys[point] - origin_y

            while end < start + count - 1:
                next_point = extended[end]
                next_dx = xs[next_point] - origin_x
                next_dy = ys[next_point] - origin_y
                cross = dx * next_dy - dy * next_dx

                if cross > 0:
                    window |= 1 << next_point
                    end += 1
                elif cross == 0 and dx * next_dx + dy * next_dy > 0:
                    end += 1
                else:
                    break

            left[origin][point] = window
            window &= ~(1 << extended[start + 1])

    return left


def buildOpenSegmentClear(points):
    count = len(points)
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    clear = [[True] * count for _ in range(count)]

    for start in range(count):
        clear[start][start] = False
        directions = collections.defaultdict(list)

        for end in range(count):
            if end == start:
                continue

            dx = xs[end] - xs[start]
            dy = ys[end] - ys[start]
            divisor = math.gcd(dx, dy)
            direction = (dx // divisor, dy // divisor)
            distance = dx * dx + dy * dy
            directions[direction].append((distance, end))

        for direction_points in directions.values():
            direction_points.sort()
            for index, (_, end) in enumerate(direction_points):
                if index > 0:
                    clear[start][end] = False

    return clear


def maximumConvexHoleArea(points):
    count = len(points)
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    left = buildLeftBitsets(points)
    segment_clear = buildOpenSegmentClear(points)
    best_twice_area = 0

    for start in range(count):
        start_x = xs[start]
        start_y = ys[start]
        candidates = [
            point
            for point in range(count)
            if point != start
            and (ys[point] > start_y or (ys[point] == start_y and xs[point] > start_x))
        ]

        if len(candidates) < 2:
            continue

        candidates.sort(
            key=lambda point: (
                math.atan2(ys[point] - start_y, xs[point] - start_x),
                (xs[point] - start_x) ** 2 + (ys[point] - start_y) ** 2,
            )
        )

        candidate_count = len(candidates)
        successors = [[] for _ in range(candidate_count)]

        for current_index in range(candidate_count - 1):
            current = candidates[current_index]
            current_left = left[start][current]
            current_dx = xs[current] - start_x
            current_dy = ys[current] - start_y

            for next_index in range(current_index + 1, candidate_count):
                next_point = candidates[next_index]
                twice_area = (
                    current_dx * (ys[next_point] - start_y)
                    - current_dy * (xs[next_point] - start_x)
                )

                if twice_area <= 0:
                    continue
                if current_left & left[current][next_point] & left[next_point][start]:
                    continue

                successors[current_index].append((next_index, twice_area))

        best_chain = [dict() for _ in range(candidate_count)]
        for current_index in range(candidate_count - 1):
            for next_index, twice_area in successors[current_index]:
                previous = best_chain[next_index].get(current_index)
                if previous is None or twice_area > previous:
                    best_chain[next_index][current_index] = twice_area

        for current_index in range(candidate_count):
            current = candidates[current_index]
            chain_values = best_chain[current_index]

            for previous_index, twice_area in chain_values.items():
                previous = candidates[previous_index]
                close_turn = (
                    (xs[current] - xs[previous]) * (start_y - ys[current])
                    - (ys[current] - ys[previous]) * (start_x - xs[current])
                )
                if close_turn > 0:
                    best_twice_area = max(best_twice_area, twice_area)

            if not segment_clear[start][current]:
                continue

            for previous_index, twice_area in chain_values.items():
                previous = candidates[previous_index]
                previous_x = xs[previous]
                previous_y = ys[previous]

                for next_index, added_area in successors[current_index]:
                    next_point = candidates[next_index]
                    turn = (
                        (xs[current] - previous_x) * (ys[next_point] - ys[current])
                        - (ys[current] - previous_y) * (xs[next_point] - xs[current])
                    )

                    if turn <= 0:
                        continue

                    new_area = twice_area + added_area
                    old_area = best_chain[next_index].get(current_index)
                    if old_area is None or new_area > old_area:
                        best_chain[next_index][current_index] = new_area

    return best_twice_area / 2


def solve(count):
    return maximumConvexHoleArea(generatePoints(count))


def runTests():
    assert solve(20) == 1049694.5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve(POINT_COUNT)
    elapsed = time.time() - start

    print("Found " + format(answer, ".1f") + " in " + str(elapsed) + " seconds.")
