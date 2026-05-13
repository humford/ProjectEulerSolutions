import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


CXX_SOURCE = r"""
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <map>
#include <vector>

static const long long MODULUS = 1000000007LL;
static const std::array<int, 10> SLOT_WEIGHTS = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4};

static std::vector<std::vector<int>> blocks;
static std::map<std::vector<int>, long long> partitionMobiusByWeights;

static long long factorial(int value) {
    long long result = 1;
    for (int factor = 2; factor <= value; ++factor) {
        result *= factor;
    }
    return result;
}

static void generatePartitions(int slot) {
    if (slot == (int)SLOT_WEIGHTS.size()) {
        std::vector<int> key;
        long long mobius = 1;

        for (const std::vector<int> &block : blocks) {
            int weight = 0;
            for (int index : block) {
                weight += SLOT_WEIGHTS[(size_t)index];
            }
            key.push_back(weight);

            int blockSize = (int)block.size();
            if ((blockSize - 1) & 1) {
                mobius = -mobius;
            }
            mobius *= factorial(blockSize - 1);
        }

        std::sort(key.begin(), key.end());
        partitionMobiusByWeights[key] += mobius;
        return;
    }

    int blockCount = (int)blocks.size();
    for (int index = 0; index < blockCount; ++index) {
        blocks[(size_t)index].push_back(slot);
        generatePartitions(slot + 1);
        blocks[(size_t)index].pop_back();
    }

    blocks.push_back(std::vector<int>{slot});
    generatePartitions(slot + 1);
    blocks.pop_back();
}

static long long powerMod(long long base, long long exponent) {
    long long result = 1;
    base %= MODULUS;
    while (exponent) {
        if (exponent & 1LL) {
            result = result * base % MODULUS;
        }
        base = base * base % MODULUS;
        exponent >>= 1LL;
    }
    return result;
}

static std::vector<int> primesUpTo(int limit) {
    std::vector<char> isComposite((size_t)limit + 1, 0);
    std::vector<int> primes;
    for (int number = 2; number <= limit; ++number) {
        if (!isComposite[(size_t)number]) {
            primes.push_back(number);
            if ((long long)number * number <= limit) {
                for (long long multiple = (long long)number * number;
                     multiple <= limit;
                     multiple += number) {
                    isComposite[(size_t)multiple] = 1;
                }
            }
        }
    }
    return primes;
}

static std::map<int, int> factorialPrimeExponentCounts(int factorialArgument) {
    std::map<int, int> counts;
    for (int prime : primesUpTo(factorialArgument)) {
        long long power = prime;
        int exponent = 0;
        while (power <= factorialArgument) {
            exponent += factorialArgument / (int)power;
            power *= prime;
        }
        ++counts[exponent];
    }
    return counts;
}

static int restrictedFactorisationCount(int factorialArgument) {
    blocks.clear();
    partitionMobiusByWeights.clear();
    generatePartitions(0);

    std::map<int, int> exponentCounts =
        factorialPrimeExponentCounts(factorialArgument);
    int maxExponent = exponentCounts.rbegin()->first;

    std::vector<int> ways((size_t)maxExponent + 1);
    long long labelledDistinct = 0;

    for (const auto &entry : partitionMobiusByWeights) {
        const std::vector<int> &weights = entry.first;
        long long mobius = entry.second % MODULUS;
        if (mobius < 0) {
            mobius += MODULUS;
        }

        std::fill(ways.begin(), ways.end(), 0);
        ways[0] = 1;
        for (int weight : weights) {
            for (int total = weight; total <= maxExponent; ++total) {
                int value = ways[(size_t)total] + ways[(size_t)total - weight];
                if (value >= MODULUS) {
                    value -= MODULUS;
                }
                ways[(size_t)total] = value;
            }
        }

        long long product = 1;
        for (const auto &countEntry : exponentCounts) {
            product = (
                product
                * powerMod(ways[(size_t)countEntry.first], countEntry.second)
            ) % MODULUS;
            if (product == 0) {
                break;
            }
        }

        labelledDistinct += mobius * product;
        labelledDistinct %= MODULUS;
    }

    long long symmetry = 2LL * 6LL * 24LL;
    return (int)(labelledDistinct * powerMod(symmetry, MODULUS - 2) % MODULUS);
}

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    int factorialArgument = std::atoi(argv[1]);
    std::cout << restrictedFactorisationCount(factorialArgument) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_636_" + digest)


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


def restrictedFactorisationCount(factorialArgument):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(factorialArgument)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def runTests():
    assert restrictedFactorisationCount(25) == 4_933
    assert restrictedFactorisationCount(100) == 693_952_493
    assert restrictedFactorisationCount(1_000) == 6_364_496


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = restrictedFactorisationCount(1_000_000) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
