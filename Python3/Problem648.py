import functools
import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_000


CXX_SOURCE = r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <vector>

static const int MODULUS = 1000000000;

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    int maxDegree = std::atoi(argv[1]);
    int maxSquare = (maxDegree + 1) * (maxDegree + 1);

    std::vector<char> isSquare((size_t)maxSquare + 3, 0);
    for (int root = 1; root * root <= maxSquare + 2; ++root) {
        isSquare[(size_t)root * root] = 1;
    }

    std::vector<int> nextOne((size_t)maxDegree + 1, 0);
    std::vector<int> nextTwo((size_t)maxDegree + 1, 0);
    std::vector<int> current((size_t)maxDegree + 1, 0);

    for (int state = maxSquare; state >= 0; --state) {
        if (state > 0 && isSquare[(size_t)state]) {
            std::fill(current.begin(), current.end(), 0);
        } else {
            int reward = isSquare[(size_t)state + 1] ? 1 : 0;
            current[0] = (nextTwo[0] + reward) % MODULUS;

            for (int degree = 1; degree <= maxDegree; ++degree) {
                long long value = (
                    (long long)nextTwo[(size_t)degree]
                    + nextOne[(size_t)degree - 1]
                    - nextTwo[(size_t)degree - 1]
                );
                if (reward && degree == 1) {
                    --value;
                }
                value %= MODULUS;
                if (value < 0) {
                    value += MODULUS;
                }
                current[(size_t)degree] = (int)value;
            }
        }

        nextTwo.swap(nextOne);
        nextOne.swap(current);
    }

    for (int degree = 0; degree <= maxDegree; ++degree) {
        if (degree) std::cout << ' ';
        std::cout << nextOne[(size_t)degree];
    }
    std::cout << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_648_" + digest)


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


@functools.lru_cache(maxsize=None)
def coefficientsUpTo(maxDegree):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(maxDegree)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [int(value) for value in result.stdout.split()]


def coefficient(index):
    value = coefficientsUpTo(index)[index]
    if value > MODULUS // 2:
        return value - MODULUS
    return value


def coefficientPrefixSum(index):
    return sum(coefficientsUpTo(index)) % MODULUS


def runTests():
    assert coefficient(0) == 1
    assert coefficient(1) == 0
    assert coefficient(5) == -18
    assert coefficient(10) == 45_176
    assert coefficientPrefixSum(10) == 53_964
    assert coefficientPrefixSum(50) == 842_418_857


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = coefficientPrefixSum(1_000) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
