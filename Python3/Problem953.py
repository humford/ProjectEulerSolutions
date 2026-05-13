from math import isqrt
import hashlib
import os
import shutil
import subprocess
import tempfile
import time


TARGET = 10**14
MODULUS = 1_000_000_007
INVERSE_SIX = pow(6, -1, MODULUS)


def sieve(limit):
    isPrime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        isPrime[0] = 0
    if limit >= 1:
        isPrime[1] = 0

    for prime in range(2, isqrt(limit) + 1):
        if isPrime[prime]:
            start = prime * prime
            isPrime[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )

    primes = [value for value in range(2, limit + 1) if isPrime[value]]
    return isPrime, primes


SIEVE_CACHE = {}


def primeData(limit):
    if limit not in SIEVE_CACHE:
        SIEVE_CACHE[limit] = sieve(limit)
    return SIEVE_CACHE[limit]


def sumSquares(limit):
    value = limit % MODULUS
    return value * (value + 1) % MODULUS * (2 * value + 1) * INVERSE_SIX % MODULUS


def kernelContribution(kernel, limit):
    if kernel > limit:
        return 0
    squareLimit = isqrt(limit // kernel)
    return (kernel % MODULUS) * sumSquares(squareLimit) % MODULUS


CPP_SOURCE = r"""
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using u64 = unsigned long long;

const int MOD = 1000000007;
const long long INVERSE_SIX = 166666668;

u64 target;
int sieveLimit;
std::vector<int> primes;
std::vector<unsigned char> isPrime;

u64 isqrt_u64(u64 value) {
    u64 root = (u64)std::sqrt((long double)value);
    while ((root + 1) <= value / (root + 1)) {
        ++root;
    }
    while (root > value / root) {
        --root;
    }
    return root;
}

long long sumSquares(u64 limit) {
    long long value = limit % MOD;
    return (((value * ((value + 1) % MOD)) % MOD) * ((2 * value + 1) % MOD) % MOD) * INVERSE_SIX % MOD;
}

long long kernelContribution(u64 kernel) {
    if (kernel > target) {
        return 0;
    }
    return (long long)(kernel % MOD) * sumSquares(isqrt_u64(target / kernel)) % MOD;
}

void buildSieve() {
    isPrime.assign((size_t)sieveLimit + 1, 1);
    isPrime[0] = 0;
    if (sieveLimit >= 1) {
        isPrime[1] = 0;
    }

    for (int prime = 2; (long long)prime * prime <= sieveLimit; ++prime) {
        if (isPrime[prime]) {
            for (long long multiple = (long long)prime * prime; multiple <= sieveLimit; multiple += prime) {
                isPrime[(size_t)multiple] = 0;
            }
        }
    }

    u64 sqrtTarget = isqrt_u64(target);
    for (int value = 2; (u64)value <= sqrtTarget; ++value) {
        if (isPrime[value]) {
            primes.push_back(value);
        }
    }
}

long long search(int nextIndex, u64 product, int xorValue, int lastPrime) {
    long long answer = 0;
    int candidate = xorValue;
    if (
        candidate > lastPrime
        && candidate <= sieveLimit
        && isPrime[candidate]
        && product <= target / (u64)candidate
    ) {
        answer = (answer + kernelContribution(product * (u64)candidate)) % MOD;
    }

    u64 remaining = target / product;
    for (int index = nextIndex; index < (int)primes.size(); ++index) {
        int prime = primes[index];
        if ((u64)prime > remaining / (u64)prime) {
            break;
        }
        answer += search(index + 1, product * (u64)prime, xorValue ^ prime, prime);
        if (answer >= MOD) {
            answer %= MOD;
        }
    }

    return answer % MOD;
}

long long computeS(u64 limit) {
    target = limit;
    u64 sqrtTarget = isqrt_u64(target);
    sieveLimit = 2;
    while ((u64)sieveLimit <= sqrtTarget) {
        sieveLimit <<= 1;
    }

    primes.clear();
    buildSieve();

    long long answer = kernelContribution(1);
    for (int index = 0; index < (int)primes.size(); ++index) {
        int prime = primes[index];
        if ((u64)prime > target / (u64)prime) {
            break;
        }
        answer += search(index + 1, prime, prime, prime);
        if (answer >= MOD) {
            answer %= MOD;
        }
    }
    return answer % MOD;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        return 2;
    }
    std::cout << computeS(std::strtoull(argv[1], nullptr, 10)) << "\n";
    return 0;
}
"""


def pythonS(limit):
    sqrtLimit = isqrt(limit)
    sieveLimit = max(2, 1 << sqrtLimit.bit_length())
    isPrime, primes = primeData(sieveLimit)

    answer = kernelContribution(1, limit)
    prefixEnd = 0
    for index, prime in enumerate(primes):
        if prime > sqrtLimit:
            break
        prefixEnd = index + 1

    stack = []
    for index in range(prefixEnd):
        prime = primes[index]
        if prime * prime > limit:
            break
        stack.append((index + 1, prime, prime, prime))

    while stack:
        nextIndex, product, xorValue, lastPrime = stack.pop()
        candidate = xorValue
        if (
            candidate > lastPrime
            and candidate <= sieveLimit
            and isPrime[candidate]
            and product * candidate <= limit
        ):
            answer = (answer + kernelContribution(product * candidate, limit)) % MODULUS

        remaining = limit // product
        for index in range(nextIndex, prefixEnd):
            prime = primes[index]
            if prime * prime > remaining:
                break
            stack.append((index + 1, product * prime, xorValue ^ prime, prime))

    return answer % MODULUS


def nativeExecutable():
    compiler = shutil.which("c++") or shutil.which("g++") or shutil.which("clang++")
    if compiler is None:
        raise RuntimeError("Problem 953 target computation requires a C++ compiler.")

    digest = hashlib.sha256(CPP_SOURCE.encode("utf-8")).hexdigest()[:16]
    base = os.path.join(tempfile.gettempdir(), "project_euler_953_" + digest)
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


def S(limit):
    executable = nativeExecutable()
    completed = subprocess.run(
        [executable, str(limit)],
        check=True,
        text=True,
        capture_output=True,
    )
    return int(completed.stdout.strip())


def bruteS(limit):
    smallestFactor = list(range(limit + 1))
    for value in range(2, isqrt(limit) + 1):
        if smallestFactor[value] == value:
            for multiple in range(value * value, limit + 1, value):
                if smallestFactor[multiple] == multiple:
                    smallestFactor[multiple] = value

    total = 1
    for value in range(2, limit + 1):
        quotient = value
        xorValue = 0
        while quotient > 1:
            prime = smallestFactor[quotient]
            parity = 0
            while quotient % prime == 0:
                quotient //= prime
                parity ^= 1
            if parity:
                xorValue ^= prime
        if xorValue == 0:
            total += value

    return total


def solve():
    return S(TARGET)


def runTests():
    assert pythonS(10) == 14
    assert pythonS(100) == 455
    assert S(10) == 14
    assert S(100) == 455
    for limit in (1, 10, 70, 100, 250):
        assert pythonS(limit) == bruteS(limit)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
