import math
import time


TARGET_N = 101


def tridiagonalSolve(lower, diagonal, upper, rhs):
    n = len(diagonal)
    c = upper[:]
    d = diagonal[:]
    b = rhs[:]

    for index in range(n - 1):
        factor = lower[index] / d[index]
        d[index + 1] -= factor * c[index]
        b[index + 1] -= factor * b[index]

    result = [0.0] * n
    result[-1] = b[-1] / d[-1]
    for index in range(n - 2, -1, -1):
        result[index] = (b[index] - c[index] * result[index + 1]) / d[index]

    return result


def maxResidual(points):
    residual = 0.0

    for index in range(1, len(points) - 1):
        a = points[index - 1]
        x = points[index]
        b = points[index + 1]
        value = a**4 - b**4 + 4 * x**3 * (b - a)
        residual = max(residual, abs(value))

    return residual


def newtonSolve(points):
    points = points[:]
    n = len(points)
    unknownCount = n - 2

    for _ in range(200):
        residuals = [0.0] * unknownCount
        diagonal = [0.0] * unknownCount
        lower = [0.0] * (unknownCount - 1)
        upper = [0.0] * (unknownCount - 1)

        for index in range(1, n - 1):
            a = points[index - 1]
            x = points[index]
            b = points[index + 1]
            row = index - 1

            residuals[row] = a**4 - b**4 + 4 * x**3 * (b - a)
            diagonal[row] = 12 * x * x * (b - a)
            if row:
                lower[row - 1] = 4 * a**3 - 4 * x**3
            if row + 1 < unknownCount:
                upper[row] = 4 * x**3 - 4 * b**3

        current = max(abs(value) for value in residuals)
        if current < 1e-15:
            break

        delta = tridiagonalSolve(
            lower,
            diagonal,
            upper,
            [-value for value in residuals],
        )

        step = 1.0
        while step > 1e-14:
            trial = points[:]
            for index, change in enumerate(delta):
                trial[index + 1] += step * change

            ordered = all(trial[index] < trial[index + 1] for index in range(n - 1))
            if ordered and -1 < trial[1] and trial[-2] < 1:
                if maxResidual(trial) < current:
                    points = trial
                    break
            step *= 0.5

    return points


def compensatedSum(values):
    total = 0.0
    compensation = 0.0

    for value in values:
        y = value - compensation
        t = total + y
        compensation = (t - total) - y
        total = t

    return total


def initialCandidates(n):
    candidates = []

    if n % 2 == 0:
        points = []
        for index in range(n):
            t = -1 + 2 * index / (n - 1)
            if t == 0:
                points.append(0.0)
            else:
                points.append(math.copysign(abs(t) ** (3 / 5), t))
        points[0] = -1.0
        points[-1] = 1.0
        candidates.append(points)
    else:
        half = (n - 1) // 2
        for moreLeft in (True, False):
            leftCount = half
            rightCount = half - 1
            if not moreLeft:
                leftCount, rightCount = rightCount, leftCount

            points = [-1.0]
            for index in range(1, leftCount + 1):
                z = 1 - index / (leftCount + 1)
                points.append(-(z ** (3 / 5)))
            for index in range(1, rightCount + 1):
                z = index / (rightCount + 1)
                points.append(z ** (3 / 5))
            points.append(1.0)
            points.sort()
            candidates.append(points)

    return candidates


def G(n):
    best = None

    for candidate in initialCandidates(n):
        points = newtonSolve(candidate)
        pieces = [
            (b - a) * (a**4 + b**4) / 2
            for a, b in zip(points, points[1:])
        ]
        area = 2 - compensatedSum(pieces)
        if best is None or area > best:
            best = area

    return best


def solve():
    return f"{G(TARGET_N):.9f}"


def runTests():
    assert abs(G(3) - 1.0) < 1e-12
    assert abs(G(5) - 1.477309771) < 5e-10
    assert solve() == "1.599827123"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
