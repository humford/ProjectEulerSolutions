import hashlib
import os
import subprocess
import tempfile
import time


CXX_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static std::vector<int> primesUpTo(int limit) {
    std::vector<char> isComposite((size_t)limit + 1, 0);
    std::vector<int> primes;
    for (int value = 2; value <= limit; ++value) {
        if (!isComposite[(size_t)value]) {
            primes.push_back(value);
            if ((int64_t)value * value <= limit) {
                for (int64_t multiple = (int64_t)value * value;
                     multiple <= limit;
                     multiple += value) {
                    isComposite[(size_t)multiple] = 1;
                }
            }
        }
    }
    return primes;
}

static __uint128_t parseUint128(const char* text) {
    __uint128_t value = 0;
    for (const char* cursor = text; *cursor; ++cursor) {
        value = value * 10 + (unsigned)(*cursor - '0');
    }
    return value;
}

static unsigned long long integerRoot(__uint128_t number, int exponent) {
    unsigned long long root = (unsigned long long)(
        std::pow((long double)number, 1.0L / exponent) + 2
    );

    auto isAtMost = [&](unsigned long long value) {
        __uint128_t power = 1;
        for (int index = 0; index < exponent; ++index) {
            power *= value;
        }
        return power <= number;
    };

    while (!isAtMost(root)) --root;
    while (isAtMost(root + 1)) ++root;
    return root;
}

static unsigned long long diceShowingOne(__uint128_t limit) {
    unsigned int maxSixthRoot = (unsigned int)integerRoot(limit, 6);
    std::vector<unsigned int> queries;
    queries.reserve(maxSixthRoot);
    for (unsigned int sixthRoot = 1; sixthRoot <= maxSixthRoot; ++sixthRoot) {
        __uint128_t sixthPower = 1;
        for (int index = 0; index < 6; ++index) {
            sixthPower *= sixthRoot;
        }
        queries.push_back((unsigned int)integerRoot(limit / sixthPower, 4));
    }
    std::sort(queries.begin(), queries.end());

    unsigned int squarefreeLimit = queries.back();
    std::vector<int> primes = primesUpTo((int)std::sqrt((long double)squarefreeLimit) + 1);

    const unsigned int segmentSize = 1u << 20;
    long long squarefreeCount = 0;
    long long mobiusPrefix = 0;
    unsigned long long answer = 0;
    size_t queryIndex = 0;

    for (unsigned int low = 1; low <= squarefreeLimit; low += segmentSize) {
        unsigned int high = std::min(squarefreeLimit, low + segmentSize - 1);
        size_t length = (size_t)high - low + 1;
        std::vector<unsigned int> remaining(length);
        std::vector<signed char> mobius(length, 1);
        std::vector<char> isSquarefree(length, 1);

        for (size_t index = 0; index < length; ++index) {
            remaining[index] = low + (unsigned int)index;
        }

        for (int prime : primes) {
            unsigned long long square = (unsigned long long)prime * prime;
            if (square > high) break;

            unsigned int start = (low + prime - 1) / prime * prime;
            for (unsigned int multiple = start; multiple <= high; multiple += prime) {
                size_t index = (size_t)multiple - low;
                if (remaining[index] % (unsigned int)prime == 0) {
                    mobius[index] = -mobius[index];
                    remaining[index] /= (unsigned int)prime;
                    while (remaining[index] % (unsigned int)prime == 0) {
                        remaining[index] /= (unsigned int)prime;
                    }
                }
            }

            unsigned int squareStart = (unsigned int)(
                ((unsigned long long)low + square - 1) / square * square
            );
            for (unsigned int multiple = squareStart;
                 multiple <= high;
                 multiple += (unsigned int)square) {
                isSquarefree[(size_t)multiple - low] = 0;
            }
        }

        for (size_t index = 0; index < length; ++index) {
            unsigned int value = low + (unsigned int)index;
            if (value > 1 && remaining[index] > 1) {
                mobius[index] = -mobius[index];
            }
            if (isSquarefree[index]) {
                ++squarefreeCount;
                mobiusPrefix += mobius[index];
            }
            while (queryIndex < queries.size() && queries[queryIndex] == value) {
                answer += (unsigned long long)((squarefreeCount + mobiusPrefix) / 2);
                ++queryIndex;
            }
        }
    }

    return answer;
}

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    std::cout << diceShowingOne(parseUint128(argv[1])) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_641_" + digest)


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


def divisorCounts(limit):
    counts = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            counts[multiple] += 1
    return counts


def diceShowingOneDirect(limit):
    counts = divisorCounts(limit)
    return sum(1 for number in range(1, limit + 1) if counts[number] % 6 == 1)


def diceShowingOne(limit):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(limit)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def runTests():
    assert diceShowingOneDirect(100) == 2
    assert diceShowingOne(100) == 2
    assert diceShowingOne(10 ** 8) == 69


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = diceShowingOne(10 ** 36)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
