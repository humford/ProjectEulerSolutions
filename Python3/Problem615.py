import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 123_454_321


CXX_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <queue>
#include <vector>

static const uint64_t MODULUS = 123454321ULL;

struct Factor {
    long double logValue;
    uint64_t unit;
    uint64_t inverseUnit;
    int e41;
    int e271;
    int replacementCount;
};

struct State {
    long double logValue;
    uint64_t serial;
    int lastIndex;
    uint64_t unit;
    int e41;
    int e271;
    int replacementCount;
};

struct GreaterState {
    bool operator()(const State& left, const State& right) const {
        if (left.logValue != right.logValue) {
            return left.logValue > right.logValue;
        }
        return left.serial > right.serial;
    }
};

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

static int64_t extendedGcd(int64_t a, int64_t b, int64_t& x, int64_t& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    int64_t nextX;
    int64_t nextY;
    int64_t gcd = extendedGcd(b, a % b, nextX, nextY);
    x = nextY;
    y = nextX - (a / b) * nextY;
    return gcd;
}

static uint64_t inverseMod(uint64_t value) {
    int64_t x;
    int64_t y;
    int64_t gcd = extendedGcd((int64_t)value, (int64_t)MODULUS, x, y);
    if (gcd != 1) std::abort();
    x %= (int64_t)MODULUS;
    if (x < 0) x += (int64_t)MODULUS;
    return (uint64_t)x;
}

static int primeSieveLimit(size_t neededOddPrimes) {
    if (neededOddPrimes < 100) return 1000;
    long double n = (long double)neededOddPrimes + 10.0L;
    long double estimate = n * (std::log(n) + std::log(std::log(n)));
    return (int)estimate + 1000;
}

static std::vector<int> oddPrimes(size_t needed) {
    int limit = primeSieveLimit(needed);
    while (true) {
        std::vector<char> isComposite((size_t)limit + 1, 0);
        for (int prime = 2; (int64_t)prime * prime <= limit; ++prime) {
            if (!isComposite[prime]) {
                for (int64_t multiple = (int64_t)prime * prime;
                     multiple <= limit;
                     multiple += prime) {
                    isComposite[(size_t)multiple] = 1;
                }
            }
        }

        std::vector<int> primes;
        primes.reserve(needed);
        for (int value = 3; value <= limit; value += 2) {
            if (!isComposite[value]) {
                primes.push_back(value);
                if (primes.size() >= needed) return primes;
            }
        }
        limit *= 2;
    }
}

static Factor oddPrimeReplacementFactor(int prime) {
    uint64_t unit = (uint64_t)prime;
    int e41 = 0;
    int e271 = 0;

    while (unit % 41 == 0) {
        unit /= 41;
        ++e41;
    }
    while (unit % 271 == 0) {
        unit /= 271;
        ++e271;
    }

    unit = multiplyMod(unit % MODULUS, inverseMod(2));
    return Factor{
        std::log((long double)prime / 2.0L),
        unit,
        inverseMod(unit),
        e41,
        e271,
        1,
    };
}

static std::vector<Factor> orderedFactors(size_t count) {
    std::vector<int> primes = oddPrimes(count);
    std::vector<Factor> factors;
    factors.reserve(count + 1);

    factors.push_back(oddPrimeReplacementFactor(3));
    factors.push_back(Factor{std::log(2.0L), 2, inverseMod(2), 0, 0, 0});
    for (size_t index = 1; index < primes.size(); ++index) {
        factors.push_back(oddPrimeReplacementFactor(primes[index]));
    }
    return factors;
}

static uint64_t multiplierMod(const State& state) {
    uint64_t result = state.unit;
    result = multiplyMod(result, powerMod(41, (uint64_t)state.e41));
    result = multiplyMod(result, powerMod(271, (uint64_t)state.e271));
    return result;
}

static uint64_t nthNumberWithPrimeFactors(
    uint64_t minimumFactorCount,
    uint64_t index
) {
    if (index == 1) return powerMod(2, minimumFactorCount);

    std::vector<Factor> factors = orderedFactors((size_t)index + 5);
    std::priority_queue<State, std::vector<State>, GreaterState> heap;
    uint64_t serial = 0;

    const Factor& first = factors[0];
    heap.push(State{
        first.logValue,
        serial++,
        0,
        first.unit,
        first.e41,
        first.e271,
        first.replacementCount,
    });

    uint64_t rank = 1;
    while (!heap.empty()) {
        State state = heap.top();
        heap.pop();
        ++rank;

        if (rank == index) {
            if ((uint64_t)state.replacementCount > minimumFactorCount) {
                std::abort();
            }
            return multiplyMod(powerMod(2, minimumFactorCount), multiplierMod(state));
        }

        const Factor& last = factors[(size_t)state.lastIndex];
        heap.push(State{
            state.logValue + last.logValue,
            serial++,
            state.lastIndex,
            multiplyMod(state.unit, last.unit),
            state.e41 + last.e41,
            state.e271 + last.e271,
            state.replacementCount + last.replacementCount,
        });

        int nextIndex = state.lastIndex + 1;
        const Factor& next = factors[(size_t)nextIndex];
        heap.push(State{
            state.logValue - last.logValue + next.logValue,
            serial++,
            nextIndex,
            multiplyMod(multiplyMod(state.unit, last.inverseUnit), next.unit),
            state.e41 - last.e41 + next.e41,
            state.e271 - last.e271 + next.e271,
            state.replacementCount - last.replacementCount + next.replacementCount,
        });
    }

    std::abort();
}

int main(int argc, char **argv) {
    if (argc != 3) return 1;
    uint64_t minimumFactorCount = std::strtoull(argv[1], nullptr, 10);
    uint64_t index = std::strtoull(argv[2], nullptr, 10);
    std::cout << nthNumberWithPrimeFactors(minimumFactorCount, index) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_615_" + digest)


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


def primeFactorCount(n):
    count = 0
    factor = 2
    while factor * factor <= n:
        while n % factor == 0:
            n //= factor
            count += 1
        factor += 1 if factor == 2 else 2
    if n > 1:
        count += 1
    return count


def bruteNumbersWithPrimeFactors(minimumFactorCount, count):
    found = []
    number = 2
    while len(found) < count:
        if primeFactorCount(number) >= minimumFactorCount:
            found.append(number)
        number += 1
    return found


def nthNumberWithPrimeFactors(minimumFactorCount, index):
    binaryPath = compileHelper()
    result = subprocess.run(
        [binaryPath, str(minimumFactorCount), str(index)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def runTests():
    assert [primeFactorCount(n) for n in (32, 48, 64, 72, 80)] == [5, 5, 6, 5, 5]
    assert bruteNumbersWithPrimeFactors(5, 10) == [32, 48, 64, 72, 80, 96, 108, 112, 120, 128]
    assert nthNumberWithPrimeFactors(5, 5) == 80
    assert nthNumberWithPrimeFactors(5, 10) == 128


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = nthNumberWithPrimeFactors(1_000_000, 1_000_000) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
