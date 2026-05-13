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

static const long long MODULUS = 1000000007LL;

static long long multiplyMod(long long left, long long right) {
    return (long long)((__int128)left * right % MODULUS);
}

static long long powerMod(long long base, long long exponent) {
    long long result = 1;
    while (exponent) {
        if (exponent & 1LL) result = multiplyMod(result, base);
        base = multiplyMod(base, base);
        exponent >>= 1LL;
    }
    return result;
}

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

static int primeExponent(int number, int prime) {
    int exponent = 0;
    while (number % prime == 0) {
        number /= prime;
        ++exponent;
    }
    return exponent;
}

static long long divisorSumPrefix(int limit) {
    std::vector<int> primes = primesUpTo(limit);
    std::vector<long long> factorialExponent(primes.size(), 0);
    std::vector<long long> factorialExponentPrefix(primes.size(), 0);
    std::vector<long long> inverseDenominator(primes.size(), 1);
    for (size_t index = 0; index < primes.size(); ++index) {
        inverseDenominator[index] = powerMod(primes[index] - 1, MODULUS - 2);
    }

    long long prefixSum = 0;
    for (int n = 1; n <= limit; ++n) {
        long long divisorSum = 1;
        for (size_t index = 0; index < primes.size() && primes[index] <= n; ++index) {
            int prime = primes[index];
            factorialExponent[index] += primeExponent(n, prime);
            factorialExponentPrefix[index] += factorialExponent[index];
            long long exponent =
                (long long)(n + 1) * factorialExponent[index] -
                2 * factorialExponentPrefix[index];
            if (exponent > 0) {
                long long geometricSum =
                    multiplyMod(
                        (powerMod(prime, exponent + 1) - 1 + MODULUS) % MODULUS,
                        inverseDenominator[index]
                    );
                divisorSum = multiplyMod(divisorSum, geometricSum);
            }
        }
        prefixSum += divisorSum;
        prefixSum %= MODULUS;
    }
    return prefixSum;
}

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    std::cout << divisorSumPrefix(std::atoi(argv[1])) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_650_" + digest)


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


def factorNumber(number):
    factors = {}
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            number //= divisor
        divisor += 1 if divisor == 2 else 2
    if number > 1:
        factors[number] = factors.get(number, 0) + 1
    return factors


def binomialProduct(number):
    product = 1
    for index in range(number + 1):
        product *= math.comb(number, index)
    return product


def divisorSum(number):
    total = 1
    for prime, exponent in factorNumber(number).items():
        total *= (prime ** (exponent + 1) - 1) // (prime - 1)
    return total


def binomialProductDivisorSum(number):
    return divisorSum(binomialProduct(number))


def divisorSumPrefixDirect(limit):
    return sum(binomialProductDivisorSum(number) for number in range(1, limit + 1))


def divisorSumPrefix(limit):
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
    assert binomialProduct(5) == 2_500
    assert binomialProductDivisorSum(5) == 5_467
    assert divisorSumPrefixDirect(5) == 5_736
    assert divisorSumPrefixDirect(10) == 141_740_594_713_218_418
    assert divisorSumPrefix(100) == 332_792_866


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisorSumPrefix(20_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
