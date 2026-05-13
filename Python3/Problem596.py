import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


C_SOURCE = r"""
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MODULUS 1000000007ULL

static uint64_t rangeSumMod(uint64_t low, uint64_t high) {
    uint64_t count = (high - low + 1ULL) % MODULUS;
    uint64_t sum = (low % MODULUS + high % MODULUS) % MODULUS;
    if (count & 1ULL) {
        sum = (sum * ((count + MODULUS) / 2ULL)) % MODULUS;
    } else {
        sum = ((sum * (count / 2ULL)) % MODULUS);
    }
    return sum;
}

static uint64_t divisorSumSummatoryMod(uint64_t limit) {
    uint64_t total = 0;
    for (uint64_t low = 1, high; low <= limit; low = high + 1ULL) {
        uint64_t quotient = limit / low;
        high = limit / quotient;
        total = (
            total +
            (quotient % MODULUS) * rangeSumMod(low, high)
        ) % MODULUS;
    }
    return total;
}

static uint64_t hyperballLatticePointsMod(uint64_t radius) {
    uint64_t squareRadius = radius * radius;
    uint64_t allDivisors = divisorSumSummatoryMod(squareRadius);
    uint64_t fourthDivisors = divisorSumSummatoryMod(squareRadius / 4ULL);
    uint64_t nonFourDivisors = (
        allDivisors + MODULUS - (4ULL * fourthDivisors) % MODULUS
    ) % MODULUS;
    return (1ULL + 8ULL * nonFourDivisors) % MODULUS;
}

int main(int argc, char **argv) {
    uint64_t radius = argc > 1 ? strtoull(argv[1], NULL, 10) : 100000000ULL;
    printf("%llu\n", (unsigned long long)hyperballLatticePointsMod(radius));
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(C_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_596_" + digest)


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


def arithmeticSum(low, high):
    return (low + high) * (high - low + 1) // 2


def divisorSumSummatory(limit):
    total = 0
    low = 1
    while low <= limit:
        quotient = limit // low
        high = limit // quotient
        total += quotient * arithmeticSum(low, high)
        low = high + 1
    return total


def hyperballLatticePoints(radius):
    squareRadius = radius * radius
    return 1 + 8 * (
        divisorSumSummatory(squareRadius)
        - 4 * divisorSumSummatory(squareRadius // 4)
    )


def hyperballLatticePointsMod(radius):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(radius)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def runTests():
    assert hyperballLatticePoints(2) == 89
    assert hyperballLatticePoints(5) == 3_121
    assert hyperballLatticePoints(100) == 493_490_641
    assert hyperballLatticePoints(10 ** 4) == 49_348_022_079_085_897


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hyperballLatticePointsMod(10 ** 8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
