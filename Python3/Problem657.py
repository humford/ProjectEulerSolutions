import hashlib
import math
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


CXX_SOURCE = r"""
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static const int64_t MODULUS = 1000000007LL;

static int64_t modPow(int64_t base, int64_t exponent) {
    int64_t result = 1;
    base %= MODULUS;
    while (exponent > 0) {
        if (exponent & 1) {
            result = result * base % MODULUS;
        }
        base = base * base % MODULUS;
        exponent >>= 1;
    }
    return result;
}

static std::vector<int> modularInverses(int limit) {
    std::vector<int> inverses((size_t)limit + 1, 0);
    if (limit >= 1) {
        inverses[1] = 1;
    }
    for (int value = 2; value <= limit; ++value) {
        inverses[(size_t)value] =
            (int)(MODULUS
                  - (MODULUS / value) * inverses[(size_t)(MODULUS % value)]
                        % MODULUS);
    }
    return inverses;
}

static int64_t powerSum(
    int alphabetSize,
    int64_t maxLength,
    const std::vector<int>& inverses
) {
    if (alphabetSize == 0) {
        return 1;
    }
    if (alphabetSize == 1) {
        return (maxLength + 1) % MODULUS;
    }

    int64_t numerator = modPow(alphabetSize, maxLength + 1) - 1;
    if (numerator < 0) {
        numerator += MODULUS;
    }
    return numerator * inverses[(size_t)alphabetSize - 1] % MODULUS;
}

static int64_t incompleteWordCount(int alphabetSize, int64_t maxLength) {
    std::vector<int> inverses = modularInverses(alphabetSize);
    int64_t total = 0;
    int64_t binomial = 1;

    for (int missing = 1; missing <= alphabetSize; ++missing) {
        binomial =
            binomial
            * (alphabetSize - missing + 1)
            % MODULUS
            * inverses[(size_t)missing]
            % MODULUS;

        int remainingLetters = alphabetSize - missing;
        int64_t words =
            powerSum(remainingLetters, maxLength, inverses);
        int64_t term = binomial * words % MODULUS;
        if (missing % 2 == 1) {
            total += term;
        } else {
            total -= term;
        }

        total %= MODULUS;
        if (total < 0) {
            total += MODULUS;
        }
    }

    return total;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 1;
    }

    int alphabetSize = std::atoi(argv[1]);
    int64_t maxLength = std::atoll(argv[2]);
    std::cout << incompleteWordCount(alphabetSize, maxLength) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_657_" + digest)


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
    )
    return binaryPath


def incompleteWordCountDirect(alphabetSize, maxLength):
    total = 0
    for missing in range(1, alphabetSize + 1):
        remainingLetters = alphabetSize - missing
        words = sum(remainingLetters ** length for length in range(maxLength + 1))
        sign = 1 if missing % 2 else -1
        total += sign * math.comb(alphabetSize, missing) * words
    return total


def incompleteWordCount(alphabetSize, maxLength):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(alphabetSize), str(maxLength)],
        text=True,
    )
    return int(output.strip())


def runTests():
    assert incompleteWordCountDirect(3, 0) == 1
    assert incompleteWordCountDirect(3, 2) == 13
    assert incompleteWordCountDirect(3, 4) == 79

    for alphabetSize, maxLength in [(3, 0), (3, 2), (3, 4), (5, 7), (8, 10)]:
        assert incompleteWordCount(alphabetSize, maxLength) == (
            incompleteWordCountDirect(alphabetSize, maxLength) % MODULUS
        )


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = incompleteWordCount(10 ** 7, 10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
