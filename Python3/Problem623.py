import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


CXX_SOURCE = r"""
#include <cstdlib>
#include <iostream>
#include <vector>

static const long long MODULUS = 1000000007LL;

static int lambdaCount(int symbolLimit) {
    int maxDepth = symbolLimit / 5 + 5;
    std::vector<std::vector<int>> exact(
        (size_t)maxDepth + 2,
        std::vector<int>((size_t)symbolLimit + 1)
    );

    for (int depth = maxDepth; depth >= 0; --depth) {
        for (int size = 1; size <= symbolLimit; ++size) {
            long long value = (size == 1 ? depth : 0);
            if (size >= 6) {
                value += exact[(size_t)depth + 1][(size_t)size - 5];
            }

            for (int leftSize = 1; leftSize <= size - 3; ++leftSize) {
                int rightSize = size - 2 - leftSize;
                value += (
                    (long long)exact[(size_t)depth][(size_t)leftSize] *
                    exact[(size_t)depth][(size_t)rightSize]
                ) % MODULUS;
                if (value >= (1LL << 62)) {
                    value %= MODULUS;
                }
            }

            exact[(size_t)depth][(size_t)size] = (int)(value % MODULUS);
        }
    }

    long long total = 0;
    for (int size = 0; size <= symbolLimit; ++size) {
        total += exact[0][(size_t)size];
        total %= MODULUS;
    }
    return (int)total;
}

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    int symbolLimit = std::atoi(argv[1]);
    std::cout << lambdaCount(symbolLimit) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_623_" + digest)


def compileHelper():
    binaryPath = helperBinaryPath()
    if os.path.exists(binaryPath):
        return binaryPath

    sourcePath = binaryPath + ".cpp"
    with open(sourcePath, "w", encoding="utf-8") as sourceFile:
        sourceFile.write(CXX_SOURCE)

    subprocess.run(
        ["c++", "-O3", "-std=c++17", sourcePath, "-o", binaryPath],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return binaryPath


def lambdaCount(symbols):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(symbols)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def lambdaCountSlow(symbols):
    maxDepth = symbols // 5 + 5
    exact = [[0] * (symbols + 1) for _ in range(maxDepth + 2)]
    for depth in range(maxDepth, -1, -1):
        for size in range(1, symbols + 1):
            value = depth if size == 1 else 0
            if size >= 6:
                value += exact[depth + 1][size - 5]

            for leftSize in range(1, size - 2):
                rightSize = size - 2 - leftSize
                value += exact[depth][leftSize] * exact[depth][rightSize]

            exact[depth][size] = value % MODULUS

    return sum(exact[0]) % MODULUS


def runTests():
    assert lambdaCountSlow(6) == 1
    assert lambdaCountSlow(9) == 2
    assert lambdaCountSlow(15) == 20
    assert lambdaCountSlow(35) == 3_166_438

    assert lambdaCount(6) == 1
    assert lambdaCount(9) == 2
    assert lambdaCount(15) == 20
    assert lambdaCount(35) == 3_166_438


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lambdaCount(2_000) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
