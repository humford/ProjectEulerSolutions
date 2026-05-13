import hashlib
import itertools
import math
import os
import subprocess
import tempfile
import time
from functools import lru_cache


MODULUS = 10 ** 9


def gcd3(a, b, c):
    return math.gcd(math.gcd(abs(a), abs(b)), abs(c))


def quaternionMatrix(a, b, c, d):
    entries = (
        a * a + b * b - c * c - d * d,
        2 * (b * c - a * d),
        2 * (b * d + a * c),
        2 * (b * c + a * d),
        a * a - b * b + c * c - d * d,
        2 * (c * d - a * b),
        2 * (b * d - a * c),
        2 * (c * d + a * b),
        a * a - b * b - c * c + d * d,
    )
    content = 0
    for entry in entries:
        content = math.gcd(content, abs(entry))
    return tuple(entry // content for entry in entries)


def determinant(matrix):
    return (
        matrix[0] * (matrix[4] * matrix[8] - matrix[5] * matrix[7])
        - matrix[1] * (matrix[3] * matrix[8] - matrix[5] * matrix[6])
        + matrix[2] * (matrix[3] * matrix[7] - matrix[4] * matrix[6])
    )


def rowSpans(matrix):
    return (
        abs(matrix[0]) + abs(matrix[1]) + abs(matrix[2]),
        abs(matrix[3]) + abs(matrix[4]) + abs(matrix[5]),
        abs(matrix[6]) + abs(matrix[7]) + abs(matrix[8]),
    )


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def latticePointPolynomial(matrix):
    columns = [
        (matrix[0], matrix[3], matrix[6]),
        (matrix[1], matrix[4], matrix[7]),
        (matrix[2], matrix[5], matrix[8]),
    ]
    volume = abs(determinant(matrix))
    faceSum = sum(
        gcd3(*cross(columns[i], columns[j]))
        for i, j in ((0, 1), (0, 2), (1, 2))
    )
    edgeSum = sum(gcd3(*column) for column in columns)
    return volume, faceSum, edgeSum


def latticePointCount(matrix, scale):
    volume, faceSum, edgeSum = latticePointPolynomial(matrix)
    return volume * scale ** 3 + faceSum * scale ** 2 + edgeSum * scale + 1


def pairValues(maximumSquareSum):
    root = math.isqrt(maximumSquareSum)
    pairs = []
    for a in range(-root, root + 1):
        for b in range(-root, root + 1):
            squareSum = a * a + b * b
            if squareSum <= maximumSquareSum:
                pairs.append((squareSum, a, b))
    pairs.sort()
    return pairs


@lru_cache(maxsize=None)
def smallLatticeTotals(n):
    maximumSquareSum = 4 * n
    pairs = pairValues(maximumSquareSum)
    ends = []
    index = 0

    for value in range(maximumSquareSum + 1):
        while index < len(pairs) and pairs[index][0] <= value:
            index += 1
        ends.append(index)

    cubeCount = 0
    latticePointTotal = 0

    for squareSum1, a, b in pairs:
        for squareSum2, c, d in pairs[: ends[maximumSquareSum - squareSum1]]:
            if squareSum1 + squareSum2 == 0:
                continue
            if (a, b, c, d) < (0, 0, 0, 0):
                continue
            if gcd3(a, b, math.gcd(c, d)) != 1:
                continue

            matrix = quaternionMatrix(a, b, c, d)
            spans = rowSpans(matrix)
            if max(spans) > n:
                continue

            maximumScale = min(n // span for span in spans)
            for scale in range(1, maximumScale + 1):
                placements = math.prod(n + 1 - scale * span for span in spans)
                cubeCount += placements
                latticePointTotal += placements * latticePointCount(matrix, scale)

    return cubeCount // 24, latticePointTotal // 24


def latticeCubeCount(n):
    return smallLatticeTotals(n)[0]


def latticePointSum(n):
    return smallLatticeTotals(n)[1]


C_SOURCE = r"""
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000000ULL
#define MOD24 24000000000ULL

typedef struct {
    short a;
    short b;
    short s;
} Pair;

static inline long long absll(long long x) { return x < 0 ? -x : x; }

static long long gcdll(long long a, long long b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

static int cmpPair(const void *left, const void *right) {
    const Pair *a = (const Pair *)left;
    const Pair *b = (const Pair *)right;
    return (int)a->s - (int)b->s;
}

static __int128 sumPowers(unsigned long long n, int power) {
    __int128 N = n;
    switch (power) {
        case 0: return N;
        case 1: return N * (N + 1) / 2;
        case 2: return N * (N + 1) * (2 * N + 1) / 6;
        case 3: {
            __int128 s = N * (N + 1) / 2;
            return s * s;
        }
        case 4:
            return N * (N + 1) * (2 * N + 1) *
                (3 * N * N + 3 * N - 1) / 30;
        case 5:
            return N * N * (N + 1) * (N + 1) *
                (2 * N * N + 2 * N - 1) / 12;
        case 6:
            return N * (N + 1) * (2 * N + 1) *
                (3 * N * N * N * N + 6 * N * N * N - 3 * N + 1) / 42;
    }
    return 0;
}

static unsigned long long scaledContribution(
    int n, long long r0, long long r1, long long r2,
    long long volume, long long faceSum, long long edgeSum
) {
    unsigned long long T = n / r0;
    if ((unsigned long long)(n / r1) < T) T = n / r1;
    if ((unsigned long long)(n / r2) < T) T = n / r2;

    unsigned long long np = (unsigned long long)n + 1;
    long long placements[4];
    long long points[4] = {1, edgeSum, faceSum, volume};
    placements[0] = (long long)(np * np * np);
    placements[1] = -(long long)(np * np) * (r0 + r1 + r2);
    placements[2] = (long long)np * (r0 * r1 + r0 * r2 + r1 * r2);
    placements[3] = -r0 * r1 * r2;

    unsigned long long answer = 0;
    for (int i = 0; i <= 3; ++i) {
        long long placement = placements[i] % (long long)MOD24;
        if (placement < 0) placement += MOD24;
        for (int j = 0; j <= 3; ++j) {
            unsigned long long term =
                (unsigned long long)(((__int128)placement *
                (points[j] % (long long)MOD24)) % MOD24);
            term = (unsigned long long)(((__int128)term *
                (unsigned long long)(sumPowers(T, i + j) % MOD24)) % MOD24);
            answer += term;
            answer %= MOD24;
        }
    }
    return answer;
}

int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : 5000;
    int maximumSquareSum = 4 * n;
    int root = 0;
    while ((root + 1) * (root + 1) <= maximumSquareSum) ++root;

    int maximumPairCount = (2 * root + 1) * (2 * root + 1);
    Pair *pairs = (Pair *)malloc(sizeof(Pair) * maximumPairCount);
    int pairCount = 0;
    for (int a = -root; a <= root; ++a) {
        for (int b = -root; b <= root; ++b) {
            int squareSum = a * a + b * b;
            if (squareSum <= maximumSquareSum) {
                pairs[pairCount++] = (Pair){(short)a, (short)b, (short)squareSum};
            }
        }
    }
    qsort(pairs, pairCount, sizeof(Pair), cmpPair);

    int *ends = (int *)malloc(sizeof(int) * (maximumSquareSum + 1));
    int position = 0;
    for (int value = 0; value <= maximumSquareSum; ++value) {
        while (position < pairCount && pairs[position].s <= value) ++position;
        ends[value] = position;
    }

    unsigned long long rawModulo = 0;
    for (int i = 0; i < pairCount; ++i) {
        int A = pairs[i].a;
        int B = pairs[i].b;
        int squareSum1 = pairs[i].s;
        int end = ends[maximumSquareSum - squareSum1];

        for (int j = 0; j < end; ++j) {
            int C = pairs[j].a;
            int D = pairs[j].b;
            int squareSum = squareSum1 + pairs[j].s;

            if (squareSum == 0) continue;
            if (A < 0 || (A == 0 && (B < 0 ||
                (B == 0 && (C < 0 || (C == 0 && D < 0)))))) continue;
            if (gcdll(gcdll(absll(A), absll(B)), gcdll(absll(C), absll(D))) != 1)
                continue;

            long long m[9] = {
                A*A + B*B - C*C - D*D, 2LL * (B*C - A*D), 2LL * (B*D + A*C),
                2LL * (B*C + A*D), A*A - B*B + C*C - D*D, 2LL * (C*D - A*B),
                2LL * (B*D - A*C), 2LL * (C*D + A*B), A*A - B*B - C*C + D*D
            };
            long long content = 0;
            for (int k = 0; k < 9; ++k) content = gcdll(content, m[k]);
            for (int k = 0; k < 9; ++k) m[k] /= content;

            long long r0 = absll(m[0]) + absll(m[1]) + absll(m[2]);
            long long r1 = absll(m[3]) + absll(m[4]) + absll(m[5]);
            long long r2 = absll(m[6]) + absll(m[7]) + absll(m[8]);
            if (r0 > n || r1 > n || r2 > n) continue;

            long long volume =
                m[0] * (m[4] * m[8] - m[5] * m[7])
                - m[1] * (m[3] * m[8] - m[5] * m[6])
                + m[2] * (m[3] * m[7] - m[4] * m[6]);
            if (volume < 0) volume = -volume;

            long long c01x = m[3] * m[7] - m[6] * m[4];
            long long c01y = m[6] * m[1] - m[0] * m[7];
            long long c01z = m[0] * m[4] - m[3] * m[1];
            long long c02x = m[3] * m[8] - m[6] * m[5];
            long long c02y = m[6] * m[2] - m[0] * m[8];
            long long c02z = m[0] * m[5] - m[3] * m[2];
            long long c12x = m[4] * m[8] - m[7] * m[5];
            long long c12y = m[7] * m[2] - m[1] * m[8];
            long long c12z = m[1] * m[5] - m[4] * m[2];
            long long faceSum =
                gcdll(gcdll(c01x, c01y), c01z)
                + gcdll(gcdll(c02x, c02y), c02z)
                + gcdll(gcdll(c12x, c12y), c12z);
            long long edgeSum =
                gcdll(gcdll(m[0], m[3]), m[6])
                + gcdll(gcdll(m[1], m[4]), m[7])
                + gcdll(gcdll(m[2], m[5]), m[8]);

            rawModulo += scaledContribution(n, r0, r1, r2, volume, faceSum, edgeSum);
            rawModulo %= MOD24;
        }
    }

    free(ends);
    free(pairs);
    printf("%llu\n", (rawModulo / 24) % MOD);
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(C_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_579_" + digest)


def compileHelper():
    binaryPath = helperBinaryPath()
    if os.path.exists(binaryPath):
        return binaryPath

    sourcePath = binaryPath + ".c"
    with open(sourcePath, "w", encoding="utf-8") as sourceFile:
        sourceFile.write(C_SOURCE)

    subprocess.run(
        ["cc", "-O3", sourcePath, "-o", binaryPath],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return binaryPath


def latticePointSumMod(n):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(n)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def runTests():
    assert latticeCubeCount(1) == 1
    assert latticeCubeCount(2) == 9
    assert latticeCubeCount(4) == 100
    assert latticeCubeCount(5) == 229
    assert latticeCubeCount(10) == 4_469
    assert latticeCubeCount(50) == 8_154_671
    assert latticePointSum(1) == 8
    assert latticePointSum(2) == 91
    assert latticePointSum(4) == 1_878
    assert latticePointSum(5) == 5_832
    assert latticePointSum(10) == 387_003
    assert latticePointSum(50) == 29_948_928_129
    assert latticePointSumMod(50) == 948_928_129


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = latticePointSumMod(5_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
