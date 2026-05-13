import math
import time


LIMIT = 100000
ORTHOCENTER = (5, 0)


def ceilDiv(numerator, denominator):
    return -((-numerator) // denominator)


def squareRootIfSquare(number):
    if number < 0:
        return None

    root = math.isqrt(number)
    if root * root == number:
        return root
    return None


def addTriangle(vertices, limit, seen, perimeters):
    if len(set(vertices)) < 3:
        return

    perimeter = 0.0
    for index in range(3):
        x1, y1 = vertices[index]
        x2, y2 = vertices[(index + 1) % 3]
        perimeter += math.hypot(x1 - x2, y1 - y2)

    if perimeter > limit + 1e-9:
        return

    triangle = tuple(sorted(vertices))
    if triangle not in seen:
        seen.add(triangle)
        perimeters.append(perimeter)


def triangleCentrePerimeterSum(limit):
    hx, hy = ORTHOCENTER
    radius_max_squared = (limit / 4.0) ** 2
    d_max = limit / 2.0
    m_limit = int(40.0 * d_max + 100.0)
    pq_limit = math.isqrt(m_limit) + 1
    seen = set()
    perimeters = []

    radius_squared = hx * hx + hy * hy
    radius_points = set()
    for x in range(-5, 6):
        y_squared = radius_squared - x * x
        y = squareRootIfSquare(y_squared)
        if y is not None:
            radius_points.add((x, y))
            radius_points.add((x, -y))

    for point in radius_points:
        addTriangle((ORTHOCENTER, point, (-point[0], -point[1])), limit, seen, perimeters)

    for p in range(pq_limit + 1):
        p_squared = p * p
        if p_squared > m_limit:
            break

        q_limit = math.isqrt(m_limit - p_squared)
        for q in range(-q_limit, q_limit + 1):
            if p == 0 and q != 1:
                continue
            if math.gcd(p, abs(q)) != 1:
                continue

            m = p_squared + q * q
            a = (40 * p) % m
            b = 100 % m
            divisor = math.gcd(a, m)
            if b % divisor != 0:
                continue

            modulus = m // divisor
            if modulus == 1:
                g0 = 0
            else:
                g0 = (b // divisor) * pow(a // divisor, -1, modulus) % modulus

            g_abs_max = int(d_max / math.sqrt(m)) + 2
            if p == 0:
                g_abs_min = 1
            elif m <= 100:
                g_abs_min = 1
            else:
                g_abs_min = max(1, (m - 100 + 40 * p - 1) // (40 * p))
            if g_abs_min > g_abs_max:
                continue

            for k in range(
                ceilDiv(-g_abs_max - g0, modulus),
                (g_abs_max - g0) // modulus + 1,
            ):
                g = g0 + k * modulus
                if g == 0 or abs(g) < g_abs_min:
                    continue

                value = 3 * g * g * m - 40 * g * p + 100
                if value <= 0 or value % m != 0:
                    continue

                t = squareRootIfSquare(value // m)
                if t is None:
                    continue

                if ((g * p + t * q) & 1) or ((g * q - t * p) & 1):
                    continue

                ax = hx - g * p
                ay = hy - g * q
                bx = (g * p + t * q) // 2
                by = (g * q - t * p) // 2
                cx = (g * p - t * q) // 2
                cy = (g * q + t * p) // 2

                if ax * ax + ay * ay > radius_max_squared + 1e-9:
                    continue

                addTriangle(((ax, ay), (bx, by), (cx, cy)), limit, seen, perimeters)

    return math.fsum(perimeters), len(perimeters)


def roundedPerimeterSum(limit):
    total, _ = triangleCentrePerimeterSum(limit)
    return format(total, ".4f")


def runTests():
    total, count = triangleCentrePerimeterSum(50)
    assert count == 9
    assert format(total, ".4f") == "291.0089"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = roundedPerimeterSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
