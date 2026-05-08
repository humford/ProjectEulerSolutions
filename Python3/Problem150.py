import time


def triangleValues(rows):
    modulus = 2 ** 20
    offset = 2 ** 19
    t = 0
    triangle = []

    for row in range(rows):
        values = []
        for _ in range(row + 1):
            t = (615949 * t + 797807) % modulus
            values.append(t - offset)
        triangle.append(values)

    return triangle


def rowPrefixes(triangle):
    prefixes = []
    for row in triangle:
        prefix = [0]
        for value in row:
            prefix.append(prefix[-1] + value)
        prefixes.append(prefix)
    return prefixes


def minimumSubTriangleSum(rows):
    prefixes = rowPrefixes(triangleValues(rows))
    best = 0

    for top in range(rows):
        totals = [0] * (top + 1)
        for bottom in range(top, rows):
            depth = bottom - top
            prefix = prefixes[bottom]
            for col in range(top + 1):
                totals[col] += prefix[col + depth + 1] - prefix[col]
                if totals[col] < best:
                    best = totals[col]

    return best


def runTests():
    triangle = triangleValues(3)
    assert triangle[0] == [273519]
    assert triangle[1] == [-153582, 450905]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimumSubTriangleSum(1000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
