import functools
import hashlib
import os
import subprocess
import tempfile
import time


CXX_SOURCE = r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <vector>

static int digitSumBase(int number, int base) {
    int sum = 0;
    while (number) {
        sum += number % base;
        number /= base;
    }
    return sum;
}

static int makeDigits(int number, int base, int *digits) {
    int length = 0;
    int reversed[64];
    while (number) {
        reversed[length++] = number % base;
        number /= base;
    }
    if (length == 0) {
        reversed[length++] = 0;
    }
    for (int index = 0; index < length; ++index) {
        digits[index] = reversed[length - 1 - index];
    }
    return length;
}

static void searchBest(
    const int *digits,
    int length,
    int base,
    int position,
    int current,
    int total,
    int number,
    const std::vector<unsigned char> &steps,
    unsigned char &best
) {
    if (best == 1) {
        return;
    }
    if (position == length) {
        int next = total + current;
        if (next < number && steps[(size_t)next] < best) {
            best = steps[(size_t)next];
        }
        return;
    }

    searchBest(
        digits,
        length,
        base,
        position + 1,
        digits[position],
        total + current,
        number,
        steps,
        best
    );
    if (best == 1) {
        return;
    }
    searchBest(
        digits,
        length,
        base,
        position + 1,
        current * base + digits[position],
        total,
        number,
        steps,
        best
    );
}

static unsigned char digitSumSteps(
    int number,
    int base,
    std::vector<unsigned char> &steps
) {
    if (number < base) {
        return 0;
    }
    if (digitSumBase(number, base) < base) {
        return 1;
    }

    int digits[64];
    int length = makeDigits(number, base, digits);
    unsigned char best = 255;
    searchBest(digits, length, base, 1, digits[0], 0, number, steps, best);
    return (unsigned char)(best + 1);
}

int main(int argc, char **argv) {
    if (argc != 4) return 1;
    int limit = std::atoi(argv[1]);
    int firstBase = std::atoi(argv[2]);
    int secondBase = std::atoi(argv[3]);

    std::vector<unsigned char> firstSteps((size_t)limit + 1, 0);
    std::vector<unsigned char> secondSteps((size_t)limit + 1, 0);
    long long total = 0;

    for (int number = 1; number <= limit; ++number) {
        firstSteps[(size_t)number] = digitSumSteps(number, firstBase, firstSteps);
        secondSteps[(size_t)number] = digitSumSteps(number, secondBase, secondSteps);
        if (firstSteps[(size_t)number] == secondSteps[(size_t)number]) {
            total += number;
        }
    }

    std::cout << total << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_637_" + digest)


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


def digitsInBase(number, base):
    digits = []
    while number:
        digits.append(number % base)
        number //= base
    return list(reversed(digits)) or [0]


def constructedSums(number, base):
    digits = digitsInBase(number, base)
    sums = set()
    for mask in range(1 << (len(digits) - 1)):
        total = 0
        current = digits[0]
        for index in range(len(digits) - 1):
            if mask & (1 << index):
                total += current
                current = digits[index + 1]
            else:
                current = current * base + digits[index + 1]
        sums.add(total + current)
    return sums


@functools.lru_cache(maxsize=None)
def digitSumSteps(number, base):
    if number < base:
        return 0
    return 1 + min(
        digitSumSteps(nextNumber, base)
        for nextNumber in constructedSums(number, base)
        if nextNumber < number
    )


def matchingStepSum(limit, firstBase, secondBase):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(limit), str(firstBase), str(secondBase)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def runTests():
    assert digitSumSteps(7, 10) == 0
    assert digitSumSteps(123, 10) == 1
    assert matchingStepSum(100, 10, 3) == 3_302


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = matchingStepSum(10 ** 7, 10, 3)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
