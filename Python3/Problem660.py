import hashlib
import os
import subprocess
import tempfile
import time


CXX_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static int baseValue;
static uint64_t fullMask;
static uint64_t baseSum;
static std::vector<int> smallestPrimeFactor;

static uint64_t integerPower(int base, int exponent) {
    uint64_t value = 1;
    for (int index = 0; index < exponent; ++index) {
        value *= (uint64_t)base;
    }
    return value;
}

static std::vector<int> buildSmallestPrimeFactor(int limit) {
    std::vector<int> spf((size_t)limit + 1, 0);
    std::vector<int> primes;
    primes.reserve((size_t)limit / 10);

    for (int value = 2; value <= limit; ++value) {
        if (spf[(size_t)value] == 0) {
            spf[(size_t)value] = value;
            primes.push_back(value);
        }
        for (int prime : primes) {
            int64_t composite = (int64_t)value * prime;
            if (composite > limit || prime > spf[(size_t)value]) {
                break;
            }
            spf[(size_t)composite] = prime;
        }
    }
    return spf;
}

static bool digitMask(uint64_t number, uint64_t& mask) {
    mask = 0;
    while (number > 0) {
        int digit = (int)(number % (uint64_t)baseValue);
        if ((mask >> digit) & 1ULL) {
            return false;
        }
        mask |= 1ULL << digit;
        number /= (uint64_t)baseValue;
    }
    return true;
}

static std::vector<std::pair<uint64_t, int>> divisorFactors(uint64_t a) {
    std::vector<std::pair<uint64_t, int>> factors;
    uint64_t value = a;
    while (value > 1) {
        int prime = smallestPrimeFactor[(size_t)value];
        int exponent = 0;
        while (value % (uint64_t)prime == 0) {
            value /= (uint64_t)prime;
            ++exponent;
        }
        factors.push_back({(uint64_t)prime, 2 * exponent});
    }

    bool foundThree = false;
    for (auto& factor : factors) {
        if (factor.first == 3) {
            ++factor.second;
            foundThree = true;
            break;
        }
    }
    if (!foundThree) {
        factors.push_back({3, 1});
    }
    return factors;
}

static void testDivisor(
    uint64_t a,
    uint64_t maskA,
    uint64_t divisor,
    int factorIndex,
    const std::vector<std::pair<uint64_t, int>>& factors
) {
    if (factorIndex < (int)factors.size()) {
        uint64_t value = 1;
        for (int exponent = 0; exponent <= factors[(size_t)factorIndex].second;
             ++exponent) {
            testDivisor(
                a,
                maskA,
                divisor * value,
                factorIndex + 1,
                factors
            );
            value *= factors[(size_t)factorIndex].first;
        }
        return;
    }

    uint64_t t = divisor;
    if (t == 0 || t >= a || ((a + t) & 1ULL)) {
        return;
    }

    uint64_t numerator = (a - t) * (3 * a + t);
    uint64_t denominator = 4 * t;
    if (numerator % denominator != 0) {
        return;
    }

    uint64_t b = numerator / denominator;
    if (b < a) {
        return;
    }
    uint64_t x = (a + t) / 2;
    uint64_t c = b + x;

    uint64_t maskB;
    uint64_t maskC;
    if (!digitMask(b, maskB) || (maskA & maskB)) {
        return;
    }
    if (!digitMask(c, maskC) || ((maskA | maskB) & maskC)) {
        return;
    }
    if ((maskA | maskB | maskC) != fullMask) {
        return;
    }
    if (c * c == a * a + a * b + b * b) {
        baseSum += c;
    }
}

static void processSmallestSide(uint64_t a, uint64_t maskA) {
    std::vector<std::pair<uint64_t, int>> factors = divisorFactors(a);
    testDivisor(a, maskA, 1, 0, factors);
}

static void generateSmallestSides(
    int length,
    int position,
    uint64_t number,
    uint64_t mask
) {
    if (position == length) {
        processSmallestSide(number, mask);
        return;
    }

    for (int digit = 0; digit < baseValue; ++digit) {
        if (((mask >> digit) & 1ULL) || (position == 0 && digit == 0)) {
            continue;
        }
        generateSmallestSides(
            length,
            position + 1,
            number * (uint64_t)baseValue + (uint64_t)digit,
            mask | (1ULL << digit)
        );
    }
}

static uint64_t pandigitalTriangleLargestSideSumForBase(int base) {
    baseValue = base;
    fullMask = (1ULL << baseValue) - 1ULL;
    baseSum = 0;

    int maxSmallestLength = baseValue / 3;
    for (int length = 1; length <= maxSmallestLength; ++length) {
        generateSmallestSides(length, 0, 0, 0);
    }
    return baseSum;
}

static uint64_t pandigitalTriangleLargestSideSum(int firstBase, int lastBase) {
    int maxSmallestSide = (int)integerPower(lastBase, lastBase / 3) - 1;
    smallestPrimeFactor = buildSmallestPrimeFactor(maxSmallestSide);

    uint64_t total = 0;
    for (int base = firstBase; base <= lastBase; ++base) {
        total += pandigitalTriangleLargestSideSumForBase(base);
    }
    return total;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 1;
    }

    int firstBase = std::atoi(argv[1]);
    int lastBase = std::atoi(argv[2]);
    std::cout << pandigitalTriangleLargestSideSum(firstBase, lastBase) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_660_" + digest)


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


def digitsInBase(number, base):
    digits = []
    while number:
        digits.append(number % base)
        number //= base
    return list(reversed(digits)) or [0]


def isPandigitalTriangle(sides, base):
    digits = []
    for side in sides:
        digits.extend(digitsInBase(side, base))
    return sorted(digits) == list(range(base))


def hasOneHundredTwentyDegreeAngle(sides):
    a, b, c = sorted(sides)
    return c * c == a * a + a * b + b * b


def pandigitalTriangleLargestSideSum(firstBase, lastBase):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(firstBase), str(lastBase)],
        text=True,
    )
    return int(output.strip())


def runTests():
    assert digitsInBase(217, 9) == [2, 6, 1]
    assert digitsInBase(248, 9) == [3, 0, 5]
    assert digitsInBase(403, 9) == [4, 8, 7]
    assert isPandigitalTriangle((217, 248, 403), 9)
    assert hasOneHundredTwentyDegreeAngle((217, 248, 403))
    assert pandigitalTriangleLargestSideSum(9, 9) == 1_082


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pandigitalTriangleLargestSideSum(9, 18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
