import hashlib
from math import isqrt
import os
import shutil
import subprocess
import tempfile
import time


TARGET_N = 10**18
TARGET_B = 120


CPP_SOURCE = r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

using i128 = __int128_t;
using u64 = unsigned long long;

u64 limitN;
std::vector<int> primes;
i128 coefficients[32][32];
i128 answer;

bool isPrime(int value) {
    if (value < 2) {
        return false;
    }
    for (int divisor = 2; divisor * divisor <= value; ++divisor) {
        if (value % divisor == 0) {
            return false;
        }
    }
    return true;
}

long long chooseValue(int n, int k) {
    if (k < 0 || k > n) {
        return 0;
    }
    if (k > n - k) {
        k = n - k;
    }

    long long result = 1;
    for (int index = 1; index <= k; ++index) {
        result = result * (n - k + index) / index;
    }
    return result;
}

void buildCoefficients() {
    for (int countOne = 0; countOne < 32; ++countOne) {
        for (int countTwo = 0; countTwo < 32; ++countTwo) {
            i128 total = 0;
            for (int selectedOne = 0; selectedOne <= countOne; ++selectedOne) {
                for (int selectedTwo = 0; selectedTwo <= countTwo; ++selectedTwo) {
                    if ((selectedOne + 2 * selectedTwo) % 3 != 0) {
                        continue;
                    }

                    long long ways =
                        chooseValue(countOne, selectedOne)
                        * chooseValue(countTwo, selectedTwo);
                    int parity =
                        (countOne - selectedOne) + (countTwo - selectedTwo);
                    if (parity % 2) {
                        total -= ways;
                    } else {
                        total += ways;
                    }
                }
            }
            coefficients[countOne][countTwo] = total;
        }
    }
}

void collectPrimes(int bound) {
    primes.clear();
    for (int value = 2; value <= bound; ++value) {
        if (value != 3 && isPrime(value)) {
            primes.push_back(value);
        }
    }
}

void search(int nextIndex, u64 product, int countOne, int countTwo) {
    answer += coefficients[countOne][countTwo] * static_cast<i128>(limitN / product);

    for (int index = nextIndex; index < static_cast<int>(primes.size()); ++index) {
        int prime = primes[index];
        if (product > limitN / static_cast<u64>(prime)) {
            break;
        }

        search(
            index + 1,
            product * static_cast<u64>(prime),
            countOne + (prime % 3 == 1 ? 1 : 0),
            countTwo + (prime % 3 == 2 ? 1 : 0)
        );
    }
}

std::string toString(i128 value) {
    if (value == 0) {
        return "0";
    }

    bool negative = value < 0;
    if (negative) {
        value = -value;
    }

    std::string digits;
    while (value > 0) {
        digits.push_back(static_cast<char>('0' + value % 10));
        value /= 10;
    }
    if (negative) {
        digits.push_back('-');
    }

    std::reverse(digits.begin(), digits.end());
    return digits;
}

i128 computeF(u64 n, int bound) {
    limitN = n;
    buildCoefficients();
    collectPrimes(bound);

    answer = 0;
    search(0, 1, 0, 0);
    return answer;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 2;
    }

    u64 n = std::strtoull(argv[1], nullptr, 10);
    int bound = std::atoi(argv[2]);
    std::cout << toString(computeF(n, bound)) << "\n";
    return 0;
}
"""


def nativeExecutable():
    compiler = shutil.which("c++") or shutil.which("g++") or shutil.which("clang++")
    if compiler is None:
        raise RuntimeError("Problem 967 requires a C++ compiler for the target count.")

    digest = hashlib.sha256(CPP_SOURCE.encode("utf-8")).hexdigest()[:16]
    base = os.path.join(tempfile.gettempdir(), "project_euler_967_" + digest)
    sourcePath = base + ".cpp"
    executablePath = base

    if not os.path.exists(executablePath):
        with open(sourcePath, "w", encoding="utf-8") as source:
            source.write(CPP_SOURCE)
        subprocess.run(
            [compiler, "-O3", "-std=c++17", sourcePath, "-o", executablePath],
            check=True,
        )

    return executablePath


def F(limit, bound):
    completed = subprocess.run(
        [nativeExecutable(), str(limit), str(bound)],
        check=True,
        text=True,
        capture_output=True,
    )
    return int(completed.stdout.strip())


def primeFactors(value):
    factors = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.add(value)
    return factors


def bruteF(limit, bound):
    total = 0
    for value in range(1, limit + 1):
        smallFactorSum = sum(factor for factor in primeFactors(value) if factor <= bound)
        if smallFactorSum % 3 == 0:
            total += 1
    return total


def solve():
    return F(TARGET_N, TARGET_B)


def runTests():
    assert bruteF(10, 4) == 5
    assert bruteF(10, 10) == 3
    assert bruteF(100, 10) == 41
    assert F(10, 4) == 5
    assert F(10, 10) == 3
    assert F(100, 10) == 41
    assert F(250, 30) == bruteF(250, 30)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
