import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


CXX_SOURCE = r"""
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static unsigned long long targetLimit;
static unsigned long long squareRootLimit;
static std::vector<int> primes;
static std::array<unsigned long long, 16> squarefreeSums;

static std::vector<int> primesUpTo(int limit) {
    std::vector<char> isComposite((size_t)limit + 1, 0);
    std::vector<int> result;
    for (int value = 2; value <= limit; ++value) {
        if (!isComposite[(size_t)value]) {
            result.push_back(value);
            if ((int64_t)value * value <= limit) {
                for (int64_t multiple = (int64_t)value * value;
                     multiple <= limit;
                     multiple += value) {
                    isComposite[(size_t)multiple] = 1;
                }
            }
        }
    }
    return result;
}

static void enumerateSquarefreeProducts(
    size_t startIndex,
    unsigned long long product,
    int primeFactorCount
) {
    squarefreeSums[(size_t)primeFactorCount] += targetLimit / product / product;

    for (size_t index = startIndex; index < primes.size(); ++index) {
        unsigned long long prime = (unsigned long long)primes[index];
        if (product > squareRootLimit / prime) break;
        enumerateSquarefreeProducts(index + 1, product * prime, primeFactorCount + 1);
    }
}

static unsigned long long chooseSmall(int n, int k) {
    if (k < 0 || k > n) return 0;
    unsigned long long result = 1;
    for (int step = 1; step <= k; ++step) {
        result = result * (unsigned long long)(n - k + step) / (unsigned long long)step;
    }
    return result;
}

static std::vector<unsigned long long> squarePrimeFactorCounts(unsigned long long limit) {
    targetLimit = limit;
    squareRootLimit = (unsigned long long)std::sqrt((long double)limit);
    while ((__uint128_t)(squareRootLimit + 1) * (squareRootLimit + 1) <= limit) {
        ++squareRootLimit;
    }
    while ((__uint128_t)squareRootLimit * squareRootLimit > limit) {
        --squareRootLimit;
    }

    primes = primesUpTo((int)squareRootLimit);
    squarefreeSums.fill(0);
    enumerateSquarefreeProducts(0, 1, 0);

    int maxPrimeFactorCount = 0;
    while (
        maxPrimeFactorCount + 1 < (int)squarefreeSums.size() &&
        squarefreeSums[(size_t)maxPrimeFactorCount + 1] != 0
    ) {
        ++maxPrimeFactorCount;
    }

    std::vector<unsigned long long> counts((size_t)maxPrimeFactorCount + 1, 0);
    for (int exactCount = 0; exactCount <= maxPrimeFactorCount; ++exactCount) {
        __int128 value = 0;
        for (int containingCount = exactCount;
             containingCount <= maxPrimeFactorCount;
             ++containingCount) {
            __int128 term =
                (__int128)chooseSmall(containingCount, exactCount) *
                squarefreeSums[(size_t)containingCount];
            if ((containingCount - exactCount) & 1) {
                value -= term;
            } else {
                value += term;
            }
        }
        counts[(size_t)exactCount] = (unsigned long long)value;
    }

    return counts;
}

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    unsigned long long limit = std::strtoull(argv[1], nullptr, 10);
    std::vector<unsigned long long> counts = squarePrimeFactorCounts(limit);
    for (size_t index = 0; index < counts.size(); ++index) {
        std::cout << index << " " << counts[index] << "\n";
    }
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_632_" + digest)


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


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)
    return [number for number, isPrime in enumerate(sieve) if isPrime]


def squarePrimeFactorCountsDirect(limit):
    counts = [0] * (limit + 1)
    for prime in primesUpTo(int(limit ** 0.5)):
        square = prime * prime
        for multiple in range(square, limit + 1, square):
            counts[multiple] += 1

    distribution = {}
    for value in range(1, limit + 1):
        distribution[counts[value]] = distribution.get(counts[value], 0) + 1
    return distribution


def squarePrimeFactorCounts(limit):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(limit)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    distribution = {}
    for line in result.stdout.splitlines():
        primeFactorCount, count = line.split()
        distribution[int(primeFactorCount)] = int(count)
    return distribution


def squarePrimeFactorProduct(limit):
    product = 1
    for count in squarePrimeFactorCounts(limit).values():
        if count:
            product = product * (count % MODULUS) % MODULUS
    return product


def countsList(distribution, length=6):
    return [distribution.get(index, 0) for index in range(length)]


def runTests():
    assert countsList(squarePrimeFactorCountsDirect(10)) == [7, 3, 0, 0, 0, 0]
    assert countsList(squarePrimeFactorCountsDirect(100)) == [61, 36, 3, 0, 0, 0]
    assert countsList(squarePrimeFactorCountsDirect(1_000)) == [608, 343, 48, 1, 0, 0]

    assert countsList(squarePrimeFactorCounts(10)) == [7, 3, 0, 0, 0, 0]
    assert countsList(squarePrimeFactorCounts(1_000)) == [608, 343, 48, 1, 0, 0]
    assert countsList(squarePrimeFactorCounts(10 ** 8)) == [
        60_792_694,
        33_539_196,
        5_329_747,
        329_028,
        9_257,
        78,
    ]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squarePrimeFactorProduct(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
