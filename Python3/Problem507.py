import math
import multiprocessing
import os
import time


TRIBONACCI_MODULUS = 10_000_000
TARGET_LIMIT = 20_000_000


def vectorNorm(x, y, z):
    return abs(x) + abs(y) + abs(z)


def bestReduction(w0, w1, w2, v0, v1, v2):
    candidates = {0}

    for wi, vi in ((w0, v0), (w1, v1), (w2, v2)):
        if vi == 0:
            continue

        quotient = wi // vi
        candidates.update((quotient - 1, quotient, quotient + 1))
        quotient = int(wi / vi)
        candidates.update((quotient - 1, quotient, quotient + 1))

    bestQuotient = 0
    bestNorm = vectorNorm(w0, w1, w2)

    for quotient in candidates:
        reducedNorm = (
            abs(w0 - quotient * v0)
            + abs(w1 - quotient * v1)
            + abs(w2 - quotient * v2)
        )

        if reducedNorm < bestNorm:
            bestNorm = reducedNorm
            bestQuotient = quotient

    return bestQuotient, bestNorm


def shortestVectorLength(firstVector, secondVector):
    v0, v1, v2 = firstVector
    w0, w1, w2 = secondVector
    firstNorm = vectorNorm(v0, v1, v2)
    secondNorm = vectorNorm(w0, w1, w2)

    while True:
        if secondNorm < firstNorm:
            v0, w0 = w0, v0
            v1, w1 = w1, v1
            v2, w2 = w2, v2
            firstNorm, secondNorm = secondNorm, firstNorm

        quotient, reducedNorm = bestReduction(w0, w1, w2, v0, v1, v2)
        if quotient == 0 or reducedNorm >= secondNorm:
            return firstNorm

        w0 -= quotient * v0
        w1 -= quotient * v1
        w2 -= quotient * v2
        secondNorm = reducedNorm


def multiplyMatrices(left, right):
    return [
        [
            sum(left[row][inner] * right[inner][col] for inner in range(3)) % TRIBONACCI_MODULUS
            for col in range(3)
        ]
        for row in range(3)
    ]


def powerMatrix(exponent):
    matrix = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]
    result = [[1 if row == col else 0 for col in range(3)] for row in range(3)]

    while exponent:
        if exponent & 1:
            result = multiplyMatrices(result, matrix)

        matrix = multiplyMatrices(matrix, matrix)
        exponent //= 2

    return result


def tribonacciTriple(index):
    matrix = powerMatrix(index)
    return (
        matrix[0][2] % TRIBONACCI_MODULUS,
        matrix[1][2] % TRIBONACCI_MODULUS,
        matrix[2][2] % TRIBONACCI_MODULUS,
    )


def chunkSum(args):
    start, count = args
    stateIndex = 12 * start - 11
    a, b, c = tribonacciTriple(stateIndex)
    total = 0

    for _ in range(count):
        r0 = a
        r1 = b
        r2 = c
        r3 = (r0 + r1 + r2) % TRIBONACCI_MODULUS
        r4 = (r1 + r2 + r3) % TRIBONACCI_MODULUS
        r5 = (r2 + r3 + r4) % TRIBONACCI_MODULUS
        r6 = (r3 + r4 + r5) % TRIBONACCI_MODULUS
        r7 = (r4 + r5 + r6) % TRIBONACCI_MODULUS
        r8 = (r5 + r6 + r7) % TRIBONACCI_MODULUS
        r9 = (r6 + r7 + r8) % TRIBONACCI_MODULUS
        r10 = (r7 + r8 + r9) % TRIBONACCI_MODULUS
        r11 = (r8 + r9 + r10) % TRIBONACCI_MODULUS
        r12 = (r9 + r10 + r11) % TRIBONACCI_MODULUS
        r13 = (r10 + r11 + r12) % TRIBONACCI_MODULUS
        r14 = (r11 + r12 + r13) % TRIBONACCI_MODULUS

        firstVector = (r0 - r1, r2 + r3, r4 * r5)
        secondVector = (r6 - r7, r8 + r9, r10 * r11)
        total += shortestVectorLength(firstVector, secondVector)

        a, b, c = r12, r13, r14

    return total


def workChunks(limit, workers):
    chunkSize = (limit + workers - 1) // workers
    chunks = []

    for worker in range(workers):
        start = worker * chunkSize + 1
        if start > limit:
            break

        count = min(chunkSize, limit - start + 1)
        chunks.append((start, count))

    return chunks


def shortestVectorSum(limit, workers=None):
    if workers is None:
        workers = min(8, os.cpu_count() or 1)

    if workers <= 1 or limit < 200_000:
        return chunkSum((1, limit))

    with multiprocessing.Pool(processes=workers) as pool:
        return sum(pool.map(chunkSum, workChunks(limit, workers)))


def runTests():
    assert shortestVectorSum(1, workers=1) == 32
    assert shortestVectorSum(10, workers=1) == 130_762_273_722


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = shortestVectorSum(TARGET_LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
