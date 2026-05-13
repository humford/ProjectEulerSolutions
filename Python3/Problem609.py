import hashlib
import math
import os
import subprocess
import tempfile
import time
from collections import Counter


MODULUS = 1_000_000_007


C_SOURCE = r"""
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MODULUS 1000000007ULL

static uint64_t piSequenceProduct(uint32_t limit) {
    uint8_t *isComposite = (uint8_t *)calloc((size_t)limit + 1, sizeof(uint8_t));
    uint32_t *primeCounts = (uint32_t *)malloc(((size_t)limit + 1) * sizeof(uint32_t));
    if (!isComposite || !primeCounts) {
        free(isComposite);
        free(primeCounts);
        return UINT64_MAX;
    }

    if (limit >= 0) isComposite[0] = 1;
    if (limit >= 1) isComposite[1] = 1;

    for (uint32_t prime = 2; (uint64_t)prime * prime <= limit; ++prime) {
        if (!isComposite[prime]) {
            for (uint64_t multiple = (uint64_t)prime * prime;
                 multiple <= limit;
                 multiple += prime) {
                isComposite[multiple] = 1;
            }
        }
    }

    uint32_t runningCount = 0;
    primeCounts[0] = 0;
    for (uint32_t value = 1; value <= limit; ++value) {
        if (!isComposite[value]) ++runningCount;
        primeCounts[value] = runningCount;
    }

    uint64_t counts[64];
    memset(counts, 0, sizeof(counts));

    for (uint32_t start = 1; start <= limit; ++start) {
        uint32_t value = start;
        uint32_t nonPrimeCount = 0;
        uint32_t index = 0;

        while (1) {
            if (isComposite[value]) ++nonPrimeCount;
            if (index >= 1) ++counts[nonPrimeCount];
            if (value == 1) break;

            value = primeCounts[value];
            ++index;
        }
    }

    uint64_t product = 1;
    for (uint32_t index = 0; index < 64; ++index) {
        if (counts[index]) {
            product = (product * (counts[index] % MODULUS)) % MODULUS;
        }
    }

    free(isComposite);
    free(primeCounts);
    return product;
}

int main(int argc, char **argv) {
    uint32_t limit = argc > 1 ? (uint32_t)strtoul(argv[1], NULL, 10) : 100000000U;
    uint64_t result = piSequenceProduct(limit);
    if (result == UINT64_MAX) return 1;
    printf("%llu\n", (unsigned long long)result);
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(C_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_609_" + digest)


def compileHelper():
    binaryPath = helperBinaryPath()
    if os.path.exists(binaryPath):
        return binaryPath

    sourcePath = binaryPath + ".c"
    with open(sourcePath, "w", encoding="utf-8") as sourceFile:
        sourceFile.write(C_SOURCE)

    subprocess.run(
        ["cc", "-O3", sourcePath, "-o", binaryPath],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return binaryPath


def primeFlagsAndCounts(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if isPrime[prime]:
            start = prime * prime
            isPrime[start:limit + 1:prime] = b"\x00" * (
                ((limit - start) // prime) + 1
            )

    primeCounts = [0] * (limit + 1)
    runningCount = 0
    for value in range(1, limit + 1):
        if isPrime[value]:
            runningCount += 1
        primeCounts[value] = runningCount

    return isPrime, primeCounts


def smallPiSequenceCounts(limit):
    isPrime, primeCounts = primeFlagsAndCounts(limit)
    counts = Counter()
    for start in range(1, limit + 1):
        value = start
        nonPrimeCount = 0
        index = 0
        while True:
            if not isPrime[value]:
                nonPrimeCount += 1
            if index >= 1:
                counts[nonPrimeCount] += 1
            if value == 1:
                break
            value = primeCounts[value]
            index += 1
    return counts


def smallPiSequenceProduct(limit):
    product = 1
    for count in smallPiSequenceCounts(limit).values():
        product *= count
    return product


def piSequenceProduct(n):
    if n <= 10_000:
        return smallPiSequenceProduct(n)

    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(n)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def runTests():
    assert smallPiSequenceCounts(10) == {0: 3, 1: 8, 2: 9, 3: 3}
    assert piSequenceProduct(10) == 648
    assert piSequenceProduct(100) == 31_038_676_032


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = piSequenceProduct(10 ** 8) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
