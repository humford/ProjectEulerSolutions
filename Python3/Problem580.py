import hashlib
import math
import os
import subprocess
import tempfile
import time


def isSquarefreeHilbertNumber(n):
    if n % 4 != 1:
        return False

    for divisor in range(5, math.isqrt(n) + 1, 4):
        if n % (divisor * divisor) == 0:
            return False

    return True


C_SOURCE = r"""
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    unsigned long long value;
    unsigned long long weight;
} Query;

static int cmpQuery(const void *left, const void *right) {
    const Query *a = (const Query *)left;
    const Query *b = (const Query *)right;
    return (a->value > b->value) - (a->value < b->value);
}

static unsigned long long isqrt64(unsigned long long n) {
    unsigned long long x = sqrt((long double)n);
    while ((x + 1) <= n / (x + 1)) ++x;
    while (x > n / x) --x;
    return x;
}

static unsigned int lowerBound(uint32_t *values, unsigned int length, uint32_t target) {
    unsigned int low = 0, high = length;
    while (low < high) {
        unsigned int mid = low + (high - low) / 2;
        if (values[mid] < target) low = mid + 1;
        else high = mid;
    }
    return low;
}

static unsigned int upperBound(uint32_t *values, unsigned int length, uint32_t target) {
    unsigned int low = 0, high = length;
    while (low < high) {
        unsigned int mid = low + (high - low) / 2;
        if (values[mid] <= target) low = mid + 1;
        else high = mid;
    }
    return low;
}

static unsigned long long oneModFourCount(unsigned long long n) {
    return (n + 3) / 4;
}

static unsigned long long squarefreeOneModFour(
    unsigned long long n, int32_t *oddMobiusPrefix
) {
    unsigned long long root = isqrt64(n);
    unsigned long long total = 0;
    unsigned long long divisor = 1;

    while (divisor <= root) {
        unsigned long long quotient = n / (divisor * divisor);
        unsigned long long nextDivisor = isqrt64(n / quotient);
        long long mobiusSum =
            (long long)oddMobiusPrefix[nextDivisor] - oddMobiusPrefix[divisor - 1];

        if (mobiusSum) {
            total += mobiusSum * (long long)oneModFourCount(quotient);
        }
        divisor = nextDivisor + 1;
    }

    return total;
}

static unsigned long long squarefreeHilbertCount(unsigned long long limit) {
    unsigned long long n = limit - 1;
    uint32_t root = (uint32_t)isqrt64(n);
    int8_t *mobius = (int8_t *)calloc((size_t)root + 1, 1);
    uint8_t *isComposite = (uint8_t *)calloc((size_t)root + 1, 1);
    uint32_t *primes = (uint32_t *)malloc(((size_t)root / 2 + 10) * sizeof(uint32_t));
    uint32_t primeCount = 0;

    mobius[1] = 1;
    for (uint32_t value = 2; value <= root; ++value) {
        if (!isComposite[value]) {
            primes[primeCount++] = value;
            mobius[value] = -1;
        }

        for (uint32_t index = 0; index < primeCount; ++index) {
            unsigned long long product = (unsigned long long)value * primes[index];
            if (product > root) break;
            isComposite[product] = 1;
            if (value % primes[index] == 0) {
                mobius[product] = 0;
                break;
            }
            mobius[product] = -mobius[value];
        }
    }

    int32_t *oddMobiusPrefix = (int32_t *)malloc(((size_t)root + 1) * sizeof(int32_t));
    int32_t mobiusSum = 0;
    for (uint32_t value = 0; value <= root; ++value) {
        if ((value & 1U) && mobius[value]) mobiusSum += mobius[value];
        oddMobiusPrefix[value] = mobiusSum;
    }

    uint32_t *threeModFourPrimes = (uint32_t *)malloc((size_t)primeCount * sizeof(uint32_t));
    uint32_t threeModFourCount = 0;
    for (uint32_t index = 0; index < primeCount; ++index) {
        if ((primes[index] & 3U) == 3U) {
            threeModFourPrimes[threeModFourCount++] = primes[index];
        }
    }

    Query *queries = (Query *)malloc(1000000 * sizeof(Query));
    uint32_t queryCount = 0;
    queries[queryCount++] = (Query){n, 1};

    unsigned long long lowPrime = 3;
    while (lowPrime <= root) {
        unsigned long long quotient = n / (lowPrime * lowPrime);
        if (quotient == 0) break;
        unsigned long long highPrime = isqrt64(n / quotient);
        if (highPrime > root) highPrime = root;

        uint32_t lowIndex = lowerBound(
            threeModFourPrimes, threeModFourCount, (uint32_t)lowPrime
        );
        uint32_t highIndex = upperBound(
            threeModFourPrimes, threeModFourCount, (uint32_t)highPrime
        );
        unsigned long long weight = highIndex - lowIndex;
        if (weight) queries[queryCount++] = (Query){quotient, weight};
        lowPrime = highPrime + 1;
    }

    qsort(queries, queryCount, sizeof(Query), cmpQuery);

    unsigned long long answer = 0;
    unsigned long long scanned = 0;
    unsigned long long smallCount = 0;
    for (uint32_t index = 0; index < queryCount; ) {
        unsigned long long value = queries[index].value;
        unsigned long long weight = 0;
        while (index < queryCount && queries[index].value == value) {
            weight += queries[index].weight;
            ++index;
        }

        unsigned long long count;
        if (value <= root) {
            while (scanned < value) {
                ++scanned;
                if ((scanned & 3ULL) == 1ULL && mobius[scanned] != 0) {
                    ++smallCount;
                }
            }
            count = smallCount;
        } else {
            count = squarefreeOneModFour(value, oddMobiusPrefix);
        }
        answer += weight * count;
    }

    free(queries);
    free(threeModFourPrimes);
    free(oddMobiusPrefix);
    free(primes);
    free(isComposite);
    free(mobius);
    return answer;
}

int main(int argc, char **argv) {
    unsigned long long limit = argc > 1 ? strtoull(argv[1], NULL, 10) : 10000000ULL;
    printf("%llu\n", squarefreeHilbertCount(limit));
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(C_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_580_" + digest)


def compileHelper():
    binaryPath = helperBinaryPath()
    if os.path.exists(binaryPath):
        return binaryPath

    sourcePath = binaryPath + ".c"
    with open(sourcePath, "w", encoding="utf-8") as sourceFile:
        sourceFile.write(C_SOURCE)

    subprocess.run(
        ["cc", "-O3", sourcePath, "-lm", "-o", binaryPath],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return binaryPath


def squarefreeHilbertCount(limit):
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
    assert [n for n in range(1, 100) if isSquarefreeHilbertNumber(n)] == [
        1,
        5,
        9,
        13,
        17,
        21,
        29,
        33,
        37,
        41,
        45,
        49,
        53,
        57,
        61,
        65,
        69,
        73,
        77,
        85,
        89,
        93,
        97,
    ]
    assert squarefreeHilbertCount(10 ** 7) == 2_327_192


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = squarefreeHilbertCount(10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
