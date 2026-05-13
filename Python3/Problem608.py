import hashlib
import math
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


CXX_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <unordered_map>
#include <vector>

static const uint64_t MODULUS = 1000000007ULL;

static uint64_t targetLimit;
static std::vector<uint64_t> selectedPrimes;
static std::vector<uint64_t> selectedRatios;
static std::unordered_map<uint64_t, uint64_t> divisorSumCache;
static uint64_t answer;

static uint64_t multiplyMod(uint64_t left, uint64_t right) {
    return (uint64_t)((__uint128_t)left * right % MODULUS);
}

static uint64_t powerMod(uint64_t base, uint64_t exponent) {
    uint64_t result = 1;
    while (exponent) {
        if (exponent & 1ULL) result = multiplyMod(result, base);
        base = multiplyMod(base, base);
        exponent >>= 1ULL;
    }
    return result;
}

static std::vector<int> primesUpTo(int limit) {
    std::vector<char> isComposite((size_t)limit + 1, 0);
    std::vector<int> primes;
    for (int value = 2; value <= limit; ++value) {
        if (!isComposite[value]) {
            primes.push_back(value);
            if ((int64_t)value * value <= limit) {
                for (int multiple = value * value;
                     multiple <= limit;
                     multiple += value) {
                    isComposite[multiple] = 1;
                }
            }
        }
    }
    return primes;
}

static uint64_t factorialExponent(int factorialLimit, int prime) {
    uint64_t exponent = 0;
    uint64_t power = (uint64_t)prime;
    while (power <= (uint64_t)factorialLimit) {
        exponent += (uint64_t)factorialLimit / power;
        power *= (uint64_t)prime;
    }
    return exponent;
}

static uint64_t divisorSummatory(uint64_t limit) {
    auto cached = divisorSumCache.find(limit);
    if (cached != divisorSumCache.end()) return cached->second;

    uint64_t total = 0;
    uint64_t left = 1;
    while (left <= limit) {
        uint64_t quotient = limit / left;
        uint64_t right = limit / quotient;
        uint64_t width = (right - left + 1) % MODULUS;
        uint64_t contribution = multiplyMod(quotient % MODULUS, width);
        total += contribution;
        if (total >= MODULUS) total %= MODULUS;
        left = right + 1;
    }
    total %= MODULUS;
    divisorSumCache[limit] = total;
    return total;
}

static void enumerateSquarefreeProducts(
    size_t startIndex,
    uint64_t product,
    uint64_t weight
) {
    uint64_t quotient = targetLimit / product;
    answer += multiplyMod(weight, divisorSummatory(quotient));
    if (answer >= MODULUS) answer %= MODULUS;

    for (size_t index = startIndex; index < selectedPrimes.size(); ++index) {
        uint64_t prime = selectedPrimes[index];
        if (product > targetLimit / prime) break;
        enumerateSquarefreeProducts(
            index + 1,
            product * prime,
            multiplyMod(weight, selectedRatios[index])
        );
    }
}

static uint64_t factorialDivisorSum(int factorialLimit, uint64_t n) {
    targetLimit = n;
    selectedPrimes.clear();
    selectedRatios.clear();
    divisorSumCache.clear();
    divisorSumCache.reserve(1 << 20);
    answer = 0;

    uint64_t baseWeight = 1;
    for (int prime : primesUpTo(factorialLimit)) {
        uint64_t exponent = factorialExponent(factorialLimit, prime);
        uint64_t constantCoefficient =
            ((exponent + 1) * (exponent + 2) / 2) % MODULUS;
        uint64_t selectedCoefficient =
            MODULUS - ((exponent * (exponent + 1) / 2) % MODULUS);
        if (selectedCoefficient == MODULUS) selectedCoefficient = 0;

        baseWeight = multiplyMod(baseWeight, constantCoefficient);
        selectedPrimes.push_back((uint64_t)prime);
        selectedRatios.push_back(
            multiplyMod(
                selectedCoefficient,
                powerMod(constantCoefficient, MODULUS - 2)
            )
        );
    }

    enumerateSquarefreeProducts(0, 1, baseWeight);
    return answer % MODULUS;
}

int main(int argc, char **argv) {
    if (argc != 3) return 1;
    int factorialLimit = std::atoi(argv[1]);
    uint64_t n = std::strtoull(argv[2], nullptr, 10);
    std::printf("%llu\n",
                (unsigned long long)factorialDivisorSum(factorialLimit, n));
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_608_" + digest)


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


def inferFactorialLimit(factorialValue):
    product = 1
    for limit in range(1, 1_000):
        product *= limit
        if product == factorialValue:
            return limit
        if product > factorialValue:
            break
    raise ValueError("expected m to be a factorial value")


def directDivisorSum(m, n):
    divisors = [divisor for divisor in range(1, m + 1) if m % divisor == 0]
    total = 0
    for divisor in divisors:
        for k in range(1, n + 1):
            value = k * divisor
            count = 0
            for factor in range(1, math.isqrt(value) + 1):
                if value % factor == 0:
                    count += 1 if factor * factor == value else 2
            total += count
    return total


def factorialDivisorSum(factorialLimit, n):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(factorialLimit), str(n)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def divisorSum(m, n):
    return factorialDivisorSum(inferFactorialLimit(m), n)


def runTests():
    assert divisorSum(math.factorial(3), 20) == directDivisorSum(math.factorial(3), 20)
    assert divisorSum(math.factorial(4), 30) == directDivisorSum(math.factorial(4), 30)
    assert divisorSum(math.factorial(3), 10 ** 2) == 3_398
    assert divisorSum(math.factorial(4), 10 ** 6) == 268_882_292


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisorSum(math.factorial(200), 10 ** 12) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
