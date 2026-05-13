import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_000


CXX_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <unordered_map>
#include <vector>

static const long long MODULUS = 1000000000LL;

static long long target;
static std::vector<long long> quotients;
static std::unordered_map<long long, int> quotientIndex;
static std::vector<long long> primeSums;
static std::vector<int> primes;
static std::vector<long long> smallPrimePrefix;
static long long answer;

static long long triangularMod(long long value) {
    long long left = value;
    long long right = value + 1;
    if (left % 2 == 0) {
        left /= 2;
    } else {
        right /= 2;
    }
    return (long long)((__int128)(left % MODULUS) * (right % MODULUS) % MODULUS);
}

static std::vector<int> primesUpTo(int limit) {
    std::vector<char> isComposite((size_t)limit + 1, 0);
    std::vector<int> result;
    for (int number = 2; number <= limit; ++number) {
        if (!isComposite[(size_t)number]) {
            result.push_back(number);
            if ((long long)number * number <= limit) {
                for (long long multiple = (long long)number * number;
                     multiple <= limit;
                     multiple += number) {
                    isComposite[(size_t)multiple] = 1;
                }
            }
        }
    }
    return result;
}

static void buildPrimeSummatoryTable() {
    quotients.clear();
    for (long long left = 1, right; left <= target; left = right + 1) {
        long long value = target / left;
        quotients.push_back(value);
        right = target / value;
    }
    std::sort(quotients.begin(), quotients.end());
    quotients.erase(
        std::unique(quotients.begin(), quotients.end()),
        quotients.end()
    );

    quotientIndex.clear();
    quotientIndex.reserve(quotients.size() * 2);
    primeSums.resize(quotients.size());
    for (int index = 0; index < (int)quotients.size(); ++index) {
        quotientIndex[quotients[(size_t)index]] = index;
        primeSums[(size_t)index] =
            (triangularMod(quotients[(size_t)index]) - 1 + MODULUS) % MODULUS;
    }

    int root = (int)std::sqrt((long double)target) + 2;
    primes = primesUpTo(root);
    smallPrimePrefix.assign(primes.size() + 1, 0);
    for (int index = 0; index < (int)primes.size(); ++index) {
        smallPrimePrefix[(size_t)index + 1] =
            (smallPrimePrefix[(size_t)index] + primes[(size_t)index]) % MODULUS;
    }

    for (int primeIndex = 0; primeIndex < (int)primes.size(); ++primeIndex) {
        long long prime = primes[(size_t)primeIndex];
        long long primeSquared = prime * prime;
        if (primeSquared > target) {
            break;
        }
        long long smallerPrimeSum = smallPrimePrefix[(size_t)primeIndex];

        for (int valueIndex = (int)quotients.size() - 1;
             valueIndex >= 0 && quotients[(size_t)valueIndex] >= primeSquared;
             --valueIndex) {
            long long value = quotients[(size_t)valueIndex];
            long long tail =
                (
                    primeSums[(size_t)quotientIndex[value / prime]]
                    - smallerPrimeSum
                    + MODULUS
                ) % MODULUS;
            primeSums[(size_t)valueIndex] =
                (
                    primeSums[(size_t)valueIndex]
                    - (long long)((__int128)(prime % MODULUS) * tail % MODULUS)
                    + MODULUS
                ) % MODULUS;
        }
    }
}

static long long primeSum(long long value) {
    return primeSums[(size_t)quotientIndex[value]];
}

static void addLargestPrimeFactorChoices(int startPrimeIndex, long long cofactor) {
    long long upper = target / cofactor;
    if (
        startPrimeIndex < (int)primes.size()
        && upper < primes[(size_t)startPrimeIndex]
    ) {
        return;
    }

    answer += (
        primeSum(upper)
        - smallPrimePrefix[(size_t)startPrimeIndex]
        + MODULUS
    ) % MODULUS;
    answer %= MODULUS;

    for (int primeIndex = startPrimeIndex;
         primeIndex < (int)primes.size();
         ++primeIndex) {
        long long prime = primes[(size_t)primeIndex];
        if (prime * prime > upper) {
            break;
        }
        addLargestPrimeFactorChoices(primeIndex, cofactor * prime);
    }
}

static long long largestPrimeFactorSum(long long limit) {
    target = limit;
    buildPrimeSummatoryTable();
    answer = 0;
    addLargestPrimeFactorChoices(0, 1);
    return answer % MODULUS;
}

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    long long limit = std::atoll(argv[1]);
    std::cout << largestPrimeFactorSum(limit) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_642_" + digest)


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


def largestPrimeFactorSumBrute(limit):
    largest = [0] * (limit + 1)
    for number in range(2, limit + 1):
        if largest[number] == 0:
            for multiple in range(number, limit + 1, number):
                largest[multiple] = number
    return sum(largest[2:]) % MODULUS


def largestPrimeFactorSum(limit):
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
    assert largestPrimeFactorSumBrute(10) == 32
    assert largestPrimeFactorSumBrute(100) == 1_915
    assert largestPrimeFactorSumBrute(10_000) == 10_118_280

    assert largestPrimeFactorSum(10) == 32
    assert largestPrimeFactorSum(100) == 1_915
    assert largestPrimeFactorSum(10_000) == 10_118_280


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestPrimeFactorSum(201_820_182_018) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
