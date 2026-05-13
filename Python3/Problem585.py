import hashlib
import math
import subprocess
import time
from array import array
from pathlib import Path


C3_HELPER_SOURCE = r"""
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>

static std::vector<char> squarefreeSieve(int limit) {
    std::vector<char> isSquarefree(limit + 1, 1);
    if (limit >= 0) {
        isSquarefree[0] = 0;
    }

    int root = static_cast<int>(std::sqrt(static_cast<double>(limit)));
    while (static_cast<long long>(root + 1) * (root + 1) <= limit) {
        ++root;
    }
    while (static_cast<long long>(root) * root > limit) {
        --root;
    }

    for (int prime = 2; prime <= root; ++prime) {
        int square = prime * prime;
        for (int multiple = square; multiple <= limit; multiple += square) {
            isSquarefree[multiple] = 0;
        }
    }

    return isSquarefree;
}

int main(int argc, char** argv) {
    long long n = argc > 1 ? std::atoll(argv[1]) : 5000000LL;
    int limit = static_cast<int>(std::sqrt(static_cast<double>(n)));
    while (static_cast<long long>(limit + 1) * (limit + 1) <= n) {
        ++limit;
    }
    while (static_cast<long long>(limit) * limit > n) {
        --limit;
    }

    std::vector<char> isSquarefree = squarefreeSieve(limit);
    long long count = 0;

    for (int p = 1; p < limit; ++p) {
        if (static_cast<long long>(p + 1) * (p + 1) > n) {
            break;
        }
        if (!isSquarefree[p]) {
            continue;
        }

        for (int q = 1; q <= limit; ++q) {
            if (!isSquarefree[q] || std::gcd(p, q) != 1) {
                continue;
            }
            long long pq = static_cast<long long>(p) * q;
            if ((pq + 1) * (p + q) > n) {
                break;
            }

            for (int r = 1; r <= limit; ++r) {
                if (!isSquarefree[r] || std::gcd(pq, static_cast<long long>(r)) != 1) {
                    continue;
                }
                long long pr = static_cast<long long>(p) * r;
                long long pqr = pq * r;
                if ((pq + r) * (pr + q) > n) {
                    break;
                }

                for (int s = 1; s <= limit; ++s) {
                    if (!isSquarefree[s] || std::gcd(pqr, static_cast<long long>(s)) != 1) {
                        continue;
                    }
                    if ((pq + static_cast<long long>(r) * s) * (pr + static_cast<long long>(q) * s) > n) {
                        break;
                    }

                    long long u = pq;
                    long long v = static_cast<long long>(r) * s;
                    long long a = pr;
                    long long b = static_cast<long long>(q) * s;
                    if (u == v || a == b) {
                        continue;
                    }

                    long long abSum = a + b;
                    for (long long w1 = 1; (u * w1 * w1 + v) * abSum <= n; ++w1) {
                        long long uW1 = u * w1;
                        long long uW1Squared = uW1 * w1;
                        for (long long w2 = 1; (uW1Squared + v * w2 * w2) * abSum <= n; ++w2) {
                            long long vW2 = v * w2;
                            long long vW2Squared = vW2 * w2;
                            long long firstSum = uW1Squared + vW2Squared;
                            for (long long w3 = 1; firstSum * (a * w3 * w3 + b) <= n; ++w3) {
                                long long aW3 = a * w3;
                                long long aW3Squared = aW3 * w3;
                                for (long long w4 = 1; firstSum * (aW3Squared + b * w4 * w4) <= n; ++w4) {
                                    long long bW4 = b * w4;
                                    long long bW4Squared = bW4 * w4;
                                    if (uW1Squared > vW2Squared && aW3Squared > bW4Squared) {
                                        if (std::gcd(uW1, vW2) == 1 && std::gcd(aW3, bW4) == 1) {
                                            long long secondSum = aW3Squared + bW4Squared;
                                            count += (n / firstSum) / secondSum;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    std::cout << count << "\n";
    return 0;
}
"""


def totientSieve(limit):
    phi = array("I", [0]) * (limit + 1)
    isComposite = bytearray(limit + 1)
    primes = []
    if limit >= 1:
        phi[1] = 1

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            phi[number] = number - 1
        for prime in primes:
            multiple = number * prime
            if multiple > limit:
                break
            isComposite[multiple] = 1
            if number % prime == 0:
                phi[multiple] = phi[number] * prime
                break
            phi[multiple] = phi[number] * (prime - 1)

    return phi


def primitivePairCounts(limit):
    totients = totientSieve(limit)
    counts = array("i", [0]) * (limit + 1)
    for total in range(3, limit + 1):
        counts[total] = totients[total] // 2

    root = math.isqrt(limit)
    for a in range(2, root + 1):
        aSquared = a * a
        maxB = math.isqrt(limit - aSquared)
        for b in range(1, min(a, maxB + 1)):
            if math.gcd(a, b) == 1:
                counts[aSquared + b * b] -= 1

    return counts


def prefixSums(values):
    sums = array("q", [0]) * len(values)
    total = 0
    for index, value in enumerate(values):
        total += int(value)
        sums[index] = total
    return sums


def groupedFloorSum(limit, prefix):
    total = 0
    start = 1
    while start <= limit:
        quotient = limit // start
        stop = limit // quotient
        total += quotient * (prefix[stop] - prefix[start - 1])
        start = stop + 1
    return int(total)


def firstFamilyCount(limit, prefix):
    return groupedFloorSum(limit, prefix)


def unorderedPairingCount(limit, prefix):
    cache = {}

    def partial(value):
        cached = cache.get(value)
        if cached is None:
            cached = groupedFloorSum(value, prefix)
            cache[value] = cached
        return cached

    total = 0
    start = 1
    while start <= limit:
        quotient = limit // start
        stop = limit // quotient
        total += int(prefix[stop] - prefix[start - 1]) * partial(quotient)
        start = stop + 1
    return int(total)


def squarefreeSieve(limit):
    isSquarefree = [True] * (limit + 1)
    isSquarefree[0] = False
    for prime in range(2, math.isqrt(limit) + 1):
        square = prime * prime
        for multiple in range(square, limit + 1, square):
            isSquarefree[multiple] = False
    return isSquarefree


def collapsedPairingCountSmall(limit):
    root = math.isqrt(limit)
    isSquarefree = squarefreeSieve(root)
    count = 0

    for p in range(1, root):
        if (p + 1) * (p + 1) > limit:
            break
        if not isSquarefree[p]:
            continue

        for q in range(1, root + 1):
            if not isSquarefree[q] or math.gcd(p, q) != 1:
                continue
            if (p * q + 1) * (p + q) > limit:
                break
            pq = p * q

            for r in range(1, root + 1):
                if not isSquarefree[r] or math.gcd(pq, r) != 1:
                    continue
                if (pq + r) * (p * r + q) > limit:
                    break
                pr = p * r
                pqr = pq * r

                for s in range(1, root + 1):
                    if not isSquarefree[s] or math.gcd(pqr, s) != 1:
                        continue
                    if (pq + r * s) * (pr + q * s) > limit:
                        break

                    u = pq
                    v = r * s
                    a = pr
                    b = q * s
                    if u == v or a == b:
                        continue

                    abSum = a + b
                    w1 = 1
                    while (u * w1 * w1 + v) * abSum <= limit:
                        uW1 = u * w1
                        uW1Squared = uW1 * w1
                        w2 = 1
                        while (uW1Squared + v * w2 * w2) * abSum <= limit:
                            vW2 = v * w2
                            vW2Squared = vW2 * w2
                            firstSum = uW1Squared + vW2Squared
                            w3 = 1
                            while firstSum * (a * w3 * w3 + b) <= limit:
                                aW3 = a * w3
                                aW3Squared = aW3 * w3
                                w4 = 1
                                while firstSum * (aW3Squared + b * w4 * w4) <= limit:
                                    bW4 = b * w4
                                    bW4Squared = bW4 * w4
                                    if uW1Squared > vW2Squared and aW3Squared > bW4Squared:
                                        if math.gcd(uW1, vW2) == 1 and math.gcd(aW3, bW4) == 1:
                                            secondSum = aW3Squared + bW4Squared
                                            count += (limit // firstSum) // secondSum
                                    w4 += 1
                                w3 += 1
                            w2 += 1
                        w1 += 1
    return count


def c3HelperPath():
    digest = hashlib.sha256(C3_HELPER_SOURCE.encode("utf-8")).hexdigest()[:16]
    sourcePath = Path("/private/tmp") / ("project_euler_585_c3_" + digest + ".cpp")
    binaryPath = Path("/private/tmp") / ("project_euler_585_c3_" + digest)

    if not binaryPath.exists():
        sourcePath.write_text(C3_HELPER_SOURCE)
        subprocess.run(["c++", "-O3", "-std=c++17", str(sourcePath), "-o", str(binaryPath)], check=True)

    return binaryPath


def collapsedPairingCount(limit):
    if limit <= 5_000:
        return collapsedPairingCountSmall(limit)

    helper = c3HelperPath()
    result = subprocess.run([str(helper), str(limit)], check=True, capture_output=True, text=True)
    return int(result.stdout.strip())


def denestableRootCount(limit):
    pairCounts = primitivePairCounts(limit)
    pairPrefix = prefixSums(pairCounts)

    firstCount = firstFamilyCount(limit, pairPrefix)
    pairCount = unorderedPairingCount(limit, pairPrefix)
    collapsedCount = collapsedPairingCount(limit)

    return firstCount + (pairCount - collapsedCount) // 2


def runTests():
    assert denestableRootCount(10) == 17
    assert denestableRootCount(15) == 46
    assert denestableRootCount(20) == 86
    assert denestableRootCount(30) == 213
    assert denestableRootCount(100) == 2_918
    assert denestableRootCount(5_000) == 11_134_074


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = denestableRootCount(5_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
