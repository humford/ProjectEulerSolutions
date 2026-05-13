import math
import time
from collections import defaultdict


LIMIT = 120


def primitivePythagoreanTriples(max_hypotenuse):
    triples = []
    max_m = math.isqrt(max_hypotenuse - 1) + 2

    for m in range(2, max_m + 1):
        for n in range(1, m):
            if (m - n) % 2 == 0 or math.gcd(m, n) != 1:
                continue

            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n

            if c <= max_hypotenuse:
                triples.append((a, b, c))

    return triples


def upperHalfDirections(max_perimeter):
    directions = [(1, 0, 1), (0, 1, 1)]

    for a, b, c in primitivePythagoreanTriples(max_perimeter):
        directions.extend(((a, b, c), (-a, b, c), (b, a, c), (-b, a, c)))

    return directions


def buildHalfPlaneDp(max_perimeter):
    directions = upperHalfDirections(max_perimeter)
    offset = max_perimeter
    width = 2 * max_perimeter + 1
    origin = offset * width + offset
    dp = [{} for _ in range(max_perimeter + 1)]
    dp[0][origin] = 1

    for dx, dy, length in directions:
        base = [None] * (max_perimeter + 1)

        for perimeter in range(max_perimeter + 1):
            if dp[perimeter]:
                base[perimeter] = list(dp[perimeter].items())

        for scale in range(1, max_perimeter // length + 1):
            scaled_length = scale * length
            delta = scale * dx * width + scale * dy

            for perimeter in range(max_perimeter - scaled_length + 1):
                states = base[perimeter]
                if not states:
                    continue

                target = dp[perimeter + scaled_length]
                for key, count in states:
                    next_key = key + delta
                    target[next_key] = target.get(next_key, 0) + count

    return dp, directions


def countFromHalfPlaneDp(limit, dp, directions):
    total = 0

    for first_perimeter in range(limit + 1):
        first_states = dp[first_perimeter]
        if not first_states:
            continue

        for second_perimeter in range(limit + 1 - first_perimeter):
            second_states = dp[second_perimeter]
            if not second_states:
                continue

            if len(first_states) <= len(second_states):
                for key, first_count in first_states.items():
                    second_count = second_states.get(key)
                    if second_count:
                        total += first_count * second_count
            else:
                for key, second_count in second_states.items():
                    first_count = first_states.get(key)
                    if first_count:
                        total += first_count * second_count

    total -= 1
    total -= sum(limit // (2 * length) for _dx, _dy, length in directions)

    return total


def pythagoreanPolygonCount(limit):
    max_perimeter = max(limit, 60)
    dp, directions = buildHalfPlaneDp(max_perimeter)

    assert countFromHalfPlaneDp(4, dp, directions) == 1
    assert countFromHalfPlaneDp(30, dp, directions) == 3655
    assert countFromHalfPlaneDp(60, dp, directions) == 891045

    return countFromHalfPlaneDp(limit, dp, directions)


def runTests():
    assert pythagoreanPolygonCount(60) == 891045


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pythagoreanPolygonCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
