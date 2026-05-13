import math
import time


LIMIT = 100000


def extendedGcd(a, b):
    if b == 0:
        return a, 1, 0

    gcd, x, y = extendedGcd(b, a % b)
    return gcd, y, x - (a // b) * y


def parameterInterval(u, v, ax, ay, radius_squared, x0, y0):
    norm = u * u + v * v
    dx = x0 - ax
    dy = y0 - ay
    a = norm
    b = 2 * (u * dx + v * dy)
    c = dx * dx + dy * dy - radius_squared
    discriminant = b * b - 4 * a * c

    if discriminant <= 0:
        return None

    sqrt_discriminant = math.isqrt(discriminant)
    denominator = 2 * a
    lower_numerator = -b - sqrt_discriminant
    upper_numerator = -b + sqrt_discriminant
    lower = -((-lower_numerator) // denominator)
    upper = (upper_numerator - 1) // denominator

    if lower > upper:
        return None

    return lower, upper


def lineHasInteriorPoint(u, v, m, k, p, q):
    norm = u * u + v * v
    ax = (u - m * v) // 2
    ay = (v + m * u) // 2
    bx = (u + m * v) // 2
    by = (v - m * u) // 2
    radius_squared = norm * (1 + m * m) // 4
    x0 = -k * q
    y0 = k * p

    first = parameterInterval(u, v, ax, ay, radius_squared, x0, y0)
    if first is None:
        return False

    second = parameterInterval(u, v, bx, by, radius_squared, x0, y0)
    if second is None:
        return False

    return max(first[0], second[0]) <= min(first[1], second[1])


def minimumEmptyMultiplier(u, v, maximum):
    norm = u * u + v * v
    gcd, p, q = extendedGcd(u, v)

    if gcd != 1:
        return None

    multiplier = 1
    while multiplier <= maximum:
        line_limit = int(
            math.floor(norm / (2.0 * (math.sqrt(1 + multiplier * multiplier) + multiplier)))
        )

        if line_limit == 0:
            return multiplier

        empty = True
        for k in range(1, line_limit + 1):
            if lineHasInteriorPoint(u, v, multiplier, k, p, q):
                empty = False
                break

        if empty:
            return multiplier

        multiplier += 2

    return None


def addNorm(norms_by_radius, radius_squared, norm):
    current = norms_by_radius.get(radius_squared)

    if current is None:
        norms_by_radius[radius_squared] = norm
        return

    if isinstance(current, int):
        if current == norm:
            return
        norms_by_radius[radius_squared] = (current, norm) if current < norm else (norm, current)
        return

    if norm not in current:
        norms_by_radius[radius_squared] = current + (norm,)


def sortedSetsIntersect(first, second):
    i = 0
    j = 0

    while i < len(first) and j < len(second):
        if first[i] == second[j]:
            return True
        if first[i] < second[j]:
            i += 1
        else:
            j += 1

    return False


def lenticularPairCount(limit):
    norm_limit = 4 * limit
    max_coordinate = math.isqrt(norm_limit)
    representations_by_norm = {}

    for u in range(1, max_coordinate + 1, 2):
        u_squared = u * u
        v_limit = math.isqrt(norm_limit - u_squared)

        for v in range(1, v_limit + 1, 2):
            if math.gcd(u, v) != 1:
                continue

            norm = u_squared + v * v
            representations_by_norm.setdefault(norm, []).append((u, v))

    norms_by_radius = {}

    for norm, representations in representations_by_norm.items():
        maximum_multiplier_squared = (4 * limit * limit) // norm - 1
        if maximum_multiplier_squared < 1:
            continue

        maximum_multiplier = math.isqrt(maximum_multiplier_squared)
        minimum_multiplier = None

        for u, v in representations:
            candidate = minimumEmptyMultiplier(u, v, maximum_multiplier)
            if candidate is not None and (
                minimum_multiplier is None or candidate < minimum_multiplier
            ):
                minimum_multiplier = candidate

        if minimum_multiplier is None:
            continue

        for multiplier in range(minimum_multiplier, maximum_multiplier + 1, 2):
            radius_squared = norm * (1 + multiplier * multiplier) // 4
            addNorm(norms_by_radius, radius_squared, norm)

    single_counts = {}
    multiple_counts = {}

    for value in norms_by_radius.values():
        if isinstance(value, int):
            single_counts[value] = single_counts.get(value, 0) + 1
        else:
            key = tuple(sorted(value))
            multiple_counts[key] = multiple_counts.get(key, 0) + 1

    total = 0
    for count in single_counts.values():
        total += count * (count + 1) // 2
    for count in multiple_counts.values():
        total += count * (count + 1) // 2

    for norms, count in multiple_counts.items():
        total += count * sum(single_counts.get(norm, 0) for norm in norms)

    multiple_items = list(multiple_counts.items())
    for i in range(len(multiple_items)):
        first_norms, first_count = multiple_items[i]
        for j in range(i + 1, len(multiple_items)):
            second_norms, second_count = multiple_items[j]
            if sortedSetsIntersect(first_norms, second_norms):
                total += first_count * second_count

    return total


def runTests():
    assert lenticularPairCount(10) == 30
    assert lenticularPairCount(100) == 3442


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lenticularPairCount(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
