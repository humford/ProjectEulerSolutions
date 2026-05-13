import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 10_007


C_SOURCE = r"""
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MODULUS 10007
#define MAX_VALUE 20012
#define TREE_SIZE 32768

static uint32_t powMod(uint32_t base, uint32_t exponent) {
    uint32_t result = 1;
    base %= MODULUS;
    while (exponent) {
        if (exponent & 1U) result = (result * base) % MODULUS;
        base = (base * base) % MODULUS;
        exponent >>= 1U;
    }
    return result;
}

static uint32_t primeLimit(uint32_t count) {
    if (count < 6) return 15;
    if (count <= 100000) return 1300000;
    if (count <= 1000000) return 16000000;
    return 190000000;
}

static void addFenwick(uint32_t *tree, uint32_t index, int32_t delta) {
    ++index;
    while (index <= TREE_SIZE) {
        tree[index] += delta;
        index += index & -index;
    }
}

static uint32_t findFenwick(uint32_t *tree, uint32_t target) {
    uint32_t index = 0;
    for (uint32_t bit = TREE_SIZE >> 1; bit; bit >>= 1U) {
        uint32_t next = index + bit;
        if (next <= TREE_SIZE && tree[next] < target) {
            index = next;
            target -= tree[next];
        }
    }
    return index;
}

static uint32_t doubledMedian(uint32_t *tree, uint32_t window) {
    if (window & 1U) {
        return 2U * findFenwick(tree, window / 2U + 1U);
    }
    return (
        findFenwick(tree, window / 2U) +
        findFenwick(tree, window / 2U + 1U)
    );
}

static uint16_t *buildSequence(uint32_t count) {
    uint32_t limit = primeLimit(count);
    uint8_t *composite = (uint8_t *)calloc((size_t)limit + 1, sizeof(uint8_t));
    uint16_t *sequence = (uint16_t *)calloc((size_t)count + 2, sizeof(uint16_t));
    if (!composite || !sequence) {
        free(composite);
        free(sequence);
        return NULL;
    }

    uint32_t found = 0;
    for (uint32_t value = 2; value <= limit && found < count; ++value) {
        if (!composite[value]) {
            ++found;
            sequence[found] = (uint16_t)powMod(value, found);
            if ((uint64_t)value * value <= limit) {
                for (uint64_t multiple = (uint64_t)value * value;
                     multiple <= limit;
                     multiple += value) {
                    composite[multiple] = 1;
                }
            }
        }
    }

    free(composite);
    if (found < count) {
        free(sequence);
        return NULL;
    }
    return sequence;
}

static uint16_t fleetingValue(uint16_t *sequence, uint32_t index) {
    return (uint16_t)(
        sequence[index] + sequence[index / 10000U + 1U]
    );
}

static uint64_t medianSumDoubled(uint32_t count, uint32_t window) {
    uint16_t *sequence = buildSequence(count);
    if (!sequence) return UINT64_MAX;

    uint32_t tree[TREE_SIZE + 1];
    memset(tree, 0, sizeof(tree));

    for (uint32_t index = 1; index <= window; ++index) {
        addFenwick(tree, fleetingValue(sequence, index), 1);
    }

    uint64_t total = doubledMedian(tree, window);
    for (uint32_t start = 2; start <= count - window + 1; ++start) {
        addFenwick(tree, fleetingValue(sequence, start - 1), -1);
        addFenwick(tree, fleetingValue(sequence, start + window - 1), 1);
        total += doubledMedian(tree, window);
    }

    free(sequence);
    return total;
}

int main(int argc, char **argv) {
    uint32_t count = argc > 1 ? (uint32_t)strtoul(argv[1], NULL, 10) : 10000000U;
    uint32_t window = argc > 2 ? (uint32_t)strtoul(argv[2], NULL, 10) : 100000U;
    uint64_t doubled = medianSumDoubled(count, window);
    if (doubled == UINT64_MAX) return 1;
    printf("%llu\n", (unsigned long long)doubled);
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(C_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_593_" + digest)


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


def primesUpToCount(count):
    limit = 15
    while True:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[0:2] = b"\x00\x00"
        for prime in range(2, int(limit ** 0.5) + 1):
            if sieve[prime]:
                start = prime * prime
                sieve[start:limit + 1:prime] = b"\x00" * (
                    ((limit - start) // prime) + 1
                )
        primes = [value for value in range(2, limit + 1) if sieve[value]]
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def buildSmallSequence(count):
    primes = primesUpToCount(count)
    sequence = [0] * (count + 2)
    for index, prime in enumerate(primes, 1):
        sequence[index] = pow(prime, index, MODULUS)
    return sequence


def fleetingValues(count):
    sequence = buildSmallSequence(count)
    return [
        sequence[index] + sequence[index // 10_000 + 1]
        for index in range(1, count + 1)
    ]


def medianString(values):
    values = sorted(values)
    length = len(values)
    if length % 2:
        doubled = 2 * values[length // 2]
    else:
        doubled = values[length // 2 - 1] + values[length // 2]
    return formatDoubledSum(doubled)


def fleetingMedian(start, stop):
    values = fleetingValues(stop)
    return medianString(values[start - 1:stop])


def formatDoubledSum(doubled):
    if doubled % 2:
        return str(doubled // 2) + ".5"
    return str(doubled // 2) + ".0"


def medianSum(count, window):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(count), str(window)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return formatDoubledSum(int(result.stdout.strip()))


def runTests():
    assert fleetingMedian(1, 10) == "2021.5"
    assert fleetingMedian(10 ** 2, 10 ** 3) == "4715.0"
    assert medianSum(100, 10) == "463628.5"
    assert medianSum(10 ** 5, 10 ** 4) == "675348207.5"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = medianSum(10 ** 7, 10 ** 5)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
