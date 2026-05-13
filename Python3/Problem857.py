import time


MOD = 1_000_000_007


def countNoMonochromaticTriangle(size):
    if size <= 1:
        return 1

    edgeIndex = {}
    index = 0
    for i in range(size):
        for j in range(i + 1, size):
            edgeIndex[(i, j)] = index
            index += 1

    triangles = []
    for i in range(size):
        for j in range(i + 1, size):
            for k in range(j + 1, size):
                triangles.append((edgeIndex[(i, j)], edgeIndex[(i, k)], edgeIndex[(j, k)]))

    total = 0
    for mask in range(1 << index):
        for a, b, c in triangles:
            color = (mask >> a) & 1
            if color == ((mask >> b) & 1) and color == ((mask >> c) & 1):
                break
        else:
            total += 1

    return total


def blockCounts():
    counts = [0] * 6
    for size in range(1, 6):
        counts[size] = countNoMonochromaticTriangle(size)
    return counts


def GExact(vertices, counts):
    factorial = [1] * (vertices + 1)
    for i in range(2, vertices + 1):
        factorial[i] = factorial[i - 1] * i

    def choose(n, k):
        return factorial[n] // (factorial[k] * factorial[n - k])

    values = [0] * (vertices + 1)
    values[0] = 1
    for n in range(1, vertices + 1):
        total = 0
        for size in range(1, min(5, n) + 1):
            total += choose(n, size) * counts[size] * values[n - size]
        values[n] = total
    return values[vertices]


def G(vertices, counts):
    coefficients = [0] * 6
    factorial = 1
    for size in range(1, 6):
        factorial *= size
        coefficients[size] = counts[size] * pow(factorial, MOD - 2, MOD) % MOD

    f0 = 1
    f1 = f2 = f3 = f4 = 0
    factorialMod = 1

    for n in range(1, vertices + 1):
        current = (
            coefficients[1] * f0
            + coefficients[2] * f1
            + coefficients[3] * f2
            + coefficients[4] * f3
            + coefficients[5] * f4
        ) % MOD
        f4, f3, f2, f1, f0 = f3, f2, f1, f0, current
        factorialMod = factorialMod * n % MOD

    return factorialMod * f0 % MOD


def runTests(counts):
    assert GExact(3, counts) == 24
    assert GExact(4, counts) == 186
    assert GExact(15, counts) == 12_472_315_010_483_328


def solve():
    counts = blockCounts()
    runTests(counts)
    return G(10_000_000, counts)


if __name__ == "__main__":
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
