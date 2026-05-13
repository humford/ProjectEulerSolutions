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
static const int64_t INVERSE_TWO = 500000004LL;

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
    int base,
    int64_t maxLength,
    const std::vector<int>& inverses
) {
    if (base == 0) {
        return 1;
    }
    if (base == 1) {
        return (maxLength + 1) % MODULUS;
    }

    int64_t numerator = modPow(base, maxLength + 1) - 1;
    if (numerator < 0) {
        numerator += MODULUS;
    }
    return numerator * inverses[(size_t)base - 1] % MODULUS;
}

static int64_t incompleteWordPrefixSum(int maxAlphabetSize, int64_t maxLength) {
    std::vector<int> inverses = modularInverses(maxAlphabetSize);
    int64_t total = 0;
    int64_t qCoefficient = 0;
    int64_t binomial = 1;
    int binomialTop = maxAlphabetSize + 1;

    for (int usedLetters = 0; usedLetters < maxAlphabetSize; ++usedLetters) {
        int64_t rhsCoefficient = binomial;
        if ((binomialTop - usedLetters) & 1) {
            rhsCoefficient = (MODULUS - rhsCoefficient) % MODULUS;
        }
        if (usedLetters == 0) {
            rhsCoefficient += 1;
            if (rhsCoefficient >= MODULUS) {
                rhsCoefficient -= MODULUS;
            }
        } else if (usedLetters == 1) {
            rhsCoefficient -= 1;
            if (rhsCoefficient < 0) {
                rhsCoefficient += MODULUS;
            }
        }

        if (usedLetters == 0) {
            qCoefficient = (MODULUS - rhsCoefficient) * INVERSE_TWO % MODULUS;
        } else {
            qCoefficient =
                (qCoefficient - rhsCoefficient + MODULUS)
                * INVERSE_TWO
                % MODULUS;
        }

        int64_t coefficient =
            ((usedLetters >= 1 ? 1 : 0) - qCoefficient + MODULUS) % MODULUS;
        total =
            (
                total
                + coefficient * powerSum(usedLetters, maxLength, inverses)
            ) % MODULUS;

        if (usedLetters + 1 < maxAlphabetSize) {
            binomial =
                binomial
                * (binomialTop - usedLetters)
                % MODULUS
                * inverses[(size_t)usedLetters + 1]
                % MODULUS;
        }
    }

    return total;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 1;
    }

    int maxAlphabetSize = std::atoi(argv[1]);
    int64_t maxLength = std::atoll(argv[2]);
    std::cout << incompleteWordPrefixSum(maxAlphabetSize, maxLength) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_658_" + digest)


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


def incompleteWordPrefixSumDirect(maxAlphabetSize, maxLength):
    return sum(
        incompleteWordCountDirect(alphabetSize, maxLength)
        for alphabetSize in range(1, maxAlphabetSize + 1)
    )


def incompleteWordPrefixSum(maxAlphabetSize, maxLength):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(maxAlphabetSize), str(maxLength)],
        text=True,
    )
    return int(output.strip())


def runTests():
    assert incompleteWordPrefixSumDirect(4, 4) == 406
    assert incompleteWordPrefixSumDirect(8, 8) == 27_902_680

    for maxAlphabetSize, maxLength in [(4, 4), (8, 8), (10, 100)]:
        assert incompleteWordPrefixSum(maxAlphabetSize, maxLength) == (
            incompleteWordPrefixSumDirect(maxAlphabetSize, maxLength) % MODULUS
        )


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = incompleteWordPrefixSum(10 ** 7, 10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
