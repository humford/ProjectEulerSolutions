import hashlib
import itertools
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_009


CXX_SOURCE = r"""
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static const long long MODULUS = 1000000009LL;

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

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    int limit = std::atoi(argv[1]);
    std::vector<int> primes = primesUpTo(limit);

    long long factorialP = 1;
    long long factorial2P = 1;
    long long factorial3P = 1;
    int pIndex = 0;
    int twoPIndex = 0;
    int threePIndex = 0;
    long long sum2 = 0;
    long long sum3 = 0;

    for (int prime : primes) {
        while (pIndex < prime) {
            ++pIndex;
            factorialP = multiplyMod(factorialP, pIndex);
        }
        while (twoPIndex < 2 * prime) {
            ++twoPIndex;
            factorial2P = multiplyMod(factorial2P, twoPIndex);
        }
        while (threePIndex < 3 * prime) {
            ++threePIndex;
            factorial3P = multiplyMod(factorial3P, threePIndex);
        }

        long long value2;
        long long value3;
        if (prime == 2) {
            value2 = 2;
            value3 = 6;
        } else {
            long long inversePrime = powerMod(prime, MODULUS - 2);
            long long inverseFactorialP = powerMod(factorialP, MODULUS - 2);
            long long inverseFactorial2P = powerMod(factorial2P, MODULUS - 2);
            long long binomial2 =
                multiplyMod(multiplyMod(factorial2P, inverseFactorialP), inverseFactorialP);
            long long binomial3 =
                multiplyMod(multiplyMod(factorial3P, inverseFactorialP), inverseFactorial2P);
            value2 = multiplyMod((binomial2 + 2LL * (prime - 1)) % MODULUS, inversePrime);
            value3 = multiplyMod((binomial3 + 3LL * (prime - 1)) % MODULUS, inversePrime);
        }

        sum2 += value2;
        sum2 %= MODULUS;
        sum3 += value3;
        sum3 %= MODULUS;
    }

    std::cout << sum2 << " " << sum3 << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_635_" + digest)


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


def subsetCount(q, n):
    count = 0
    for subset in itertools.combinations(range(1, q * n + 1), n):
        if sum(subset) % n == 0:
            count += 1
    return count


def subsetPrimeSums(limit):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(limit)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    sum2, sum3 = result.stdout.split()
    return int(sum2), int(sum3)


def subsetPrimeSum(q, limit):
    sum2, sum3 = subsetPrimeSums(limit)
    if q == 2:
        return sum2
    if q == 3:
        return sum3
    raise ValueError("only q=2 and q=3 are needed")


def targetSum(limit):
    return sum(subsetPrimeSums(limit)) % MODULUS


def runTests():
    assert subsetCount(2, 5) == 52
    assert subsetCount(3, 5) == 603
    assert subsetPrimeSum(2, 10) == 554
    assert subsetPrimeSum(2, 100) == 100_433_628
    assert subsetPrimeSum(3, 100) == 855_618_282


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = targetSum(10 ** 8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
