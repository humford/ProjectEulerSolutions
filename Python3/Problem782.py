import time
from math import isqrt


def countComplexityAtMost3(n):
    nSquared = n * n
    half = nSquared // 2
    seen = bytearray(half + 1)

    # Orbit 1: k = x*y, plus complement symmetry.
    for y in range(1, n + 1):
        ySquared = y * y
        end = min(ySquared, half)
        seen[0:end + 1:y] = b"\x01" * (end // y + 1)

        if ySquared > half:
            firstX = half // y + 1
            if firstX <= y:
                start = nSquared - ySquared
                end = nSquared - y * firstX
                seen[start:end + 1:y] = b"\x01" * ((end - start) // y + 1)

    seen[0] = 1

    # Orbit 2: k = v^2 - d^2.
    for v in range(n + 1):
        vSquared = v * v
        if vSquared <= half:
            dSquared = 0
            step = 1
            for _ in range(v + 1):
                seen[vSquared - dSquared] = 1
                dSquared += step
                step += 2
        else:
            firstD = isqrt(vSquared - half - 1) + 1
            complementOffset = nSquared - vSquared
            dSquared = 0
            step = 1
            for _ in range(firstD):
                seen[complementOffset + dSquared] = 1
                dSquared += step
                step += 2
            for _ in range(firstD, v + 1):
                seen[vSquared - dSquared] = 1
                dSquared += step
                step += 2

    # q(b) = 2*b*(n-b), stored only up to the symmetric midpoint.
    maxBGlobal = n // 2
    q = [0] * (maxBGlobal + 1)
    current = 0
    delta = 2 * (n - 1)
    for b in range(maxBGlobal):
        q[b] = current
        current += delta
        delta -= 4
    q[maxBGlobal] = current

    # Orbits 3-6 depend on s=a+b and ab=a(s-a).
    for s in range(n + 1):
        c = n - s
        cSquared = c * c
        cTimes2NMinusC = c * (2 * n - c)
        cTimesS = c * s

        if s % 2 == 0:
            v = s // 2
            base = v * v
            dSquared = 0
            step = 1
            for _ in range(v + 1):
                ab = base - dSquared
                twoAB = 2 * ab

                for k in (
                    cSquared + twoAB,
                    cTimes2NMinusC + twoAB,
                    cTimesS + ab,
                    2 * (cTimesS + ab),
                ):
                    if k > half:
                        k = nSquared - k
                    seen[k] = 1

                dSquared += step
                step += 2
        else:
            v = s // 2
            base = v * (v + 1)
            dProduct = 0
            step = 2
            for _ in range(v + 1):
                ab = base - dProduct
                twoAB = 2 * ab

                for k in (
                    cSquared + twoAB,
                    cTimes2NMinusC + twoAB,
                    cTimesS + ab,
                    2 * (cTimesS + ab),
                ):
                    if k > half:
                        k = nSquared - k
                    seen[k] = 1

                dProduct += step
                step += 2

    # Orbit 7: k = c^2 + 2*b*(n-b).
    for c in range(n + 1):
        cSquared = c * c
        maxB = min(n - c, maxBGlobal)
        for b in range(maxB + 1):
            k = cSquared + q[b]
            if k > half:
                k = nSquared - k
            seen[k] = 1

    halfCount = sum(seen)
    if nSquared % 2:
        return 2 * halfCount
    return 2 * halfCount - seen[half]


def countComplexityExactly2(n):
    nSquared = n * n
    values = set()

    for a in range(n + 1):
        square = a * a
        rectangle = 2 * a * (n - a)
        values.add(square)
        values.add(nSquared - square)
        values.add(rectangle)
        values.add(nSquared - rectangle)

    values.discard(0)
    values.discard(nSquared)
    return len(values)


def C(n):
    if n == 0:
        return 0
    if n == 1:
        return 2

    totalK = n * n + 1
    complexityAtMost3 = countComplexityAtMost3(n)
    complexity4 = totalK - complexityAtMost3
    complexity2 = countComplexityExactly2(n)

    return 3 * totalK - 4 - complexity2 + complexity4


def runTests():
    assert C(2) == 8
    assert C(5) == 64
    assert C(10) == 274
    assert C(20) == 1150


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = C(10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
