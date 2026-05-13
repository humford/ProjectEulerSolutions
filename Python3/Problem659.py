import hashlib
import os
import subprocess
import tempfile
import time


LAST_DIGITS_MODULUS = 10 ** 18


CXX_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static const uint64_t LAST_DIGITS_MODULUS = 1000000000000000000ULL;

static uint64_t largestPrimeSum(int limit) {
    std::vector<uint64_t> remaining((size_t)limit + 1, 0);
    std::vector<uint64_t> largestFactor((size_t)limit + 1, 0);

    for (int index = 1; index <= limit; ++index) {
        remaining[(size_t)index] = 4ULL * index * index + 1ULL;
    }

    for (int index = 1; index <= limit; ++index) {
        uint64_t factor = remaining[(size_t)index];
        if (factor == 1) {
            continue;
        }

        largestFactor[(size_t)index] =
            std::max(largestFactor[(size_t)index], factor);

        for (uint64_t next = factor + (uint64_t)index;
             next <= (uint64_t)limit;
             next += factor) {
            largestFactor[(size_t)next] =
                std::max(largestFactor[(size_t)next], factor);
            while (remaining[(size_t)next] % factor == 0) {
                remaining[(size_t)next] /= factor;
            }
        }

        if (factor > (uint64_t)index) {
            for (uint64_t next = factor - (uint64_t)index;
                 next <= (uint64_t)limit;
                 next += factor) {
                if (next == 0) {
                    continue;
                }
                largestFactor[(size_t)next] =
                    std::max(largestFactor[(size_t)next], factor);
                while (remaining[(size_t)next] % factor == 0) {
                    remaining[(size_t)next] /= factor;
                }
            }
        }
    }

    uint64_t total = 0;
    for (int index = 1; index <= limit; ++index) {
        total += largestFactor[(size_t)index] % LAST_DIGITS_MODULUS;
        total %= LAST_DIGITS_MODULUS;
    }
    return total;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        return 1;
    }

    int limit = std::atoi(argv[1]);
    std::cout << largestPrimeSum(limit) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_659_" + digest)


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


def largestPrimeFactor(number):
    largest = 1
    factor = 2
    while factor * factor <= number:
        while number % factor == 0:
            largest = factor
            number //= factor
        factor += 1 if factor == 2 else 2
    return max(largest, number)


def largestSharedPrimeForConstant(constant):
    return largestPrimeFactor(4 * constant + 1)


def largestPrimeForParameter(parameter):
    return largestPrimeFactor(4 * parameter * parameter + 1)


def largestPrimeSum(limit):
    binaryPath = compileHelper()
    output = subprocess.check_output([binaryPath, str(limit)], text=True)
    return int(output.strip())


def runTests():
    assert largestSharedPrimeForConstant(3) == 13
    assert largestPrimeForParameter(3) == 37
    for limit in [10, 100, 1_000]:
        assert largestPrimeSum(limit) == sum(
            largestPrimeForParameter(parameter)
            for parameter in range(1, limit + 1)
        )


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestPrimeSum(10_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
