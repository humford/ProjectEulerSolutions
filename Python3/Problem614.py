import hashlib
import os
import subprocess
import tempfile
import textwrap
import time


MODULUS = 1_000_000_007


HELPER_SOURCE = r"""
#include <cstdlib>
#include <iostream>
#include <vector>

using namespace std;

static const int MODULUS = 1000000007;

int specialPartitionPrefixSum(int limit) {
    int maxReciprocalThetaIndex = limit / 4;
    vector<int> reciprocalTheta(maxReciprocalThetaIndex + 1);
    vector<int> reciprocalThetaPrefix(maxReciprocalThetaIndex + 1);
    reciprocalTheta[0] = 1;
    reciprocalThetaPrefix[0] = 1;

    // If J(q) = 1 / phi(-q), then
    // (1 + 2 * sum_{k>=1} (-1)^k q^{k*k}) * J(q) = 1.
    for (int n = 1; n <= maxReciprocalThetaIndex; ++n) {
        long long alternatingSum = 0;
        for (long long k = 1, square = 1; square <= n; ++k, square = k * k) {
            if (k & 1) {
                alternatingSum += reciprocalTheta[n - square];
            } else {
                alternatingSum -= reciprocalTheta[n - square];
            }
        }
        alternatingSum %= MODULUS;
        if (alternatingSum < 0) {
            alternatingSum += MODULUS;
        }
        reciprocalTheta[n] = (2 * alternatingSum) % MODULUS;
        reciprocalThetaPrefix[n] =
            (reciprocalThetaPrefix[n - 1] + reciprocalTheta[n]) % MODULUS;
    }

    long long answer = 0;
    for (long long r = 0;; ++r) {
        long long triangular = r * (r + 1) / 2;
        if (triangular > limit) {
            break;
        }
        answer += reciprocalThetaPrefix[(limit - triangular) / 4];
        answer %= MODULUS;
    }

    // The convolution above includes the constant term P(0); the problem asks
    // for the sum from P(1) through P(limit).
    answer = (answer + MODULUS - 1) % MODULUS;
    return (int)answer;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        return 2;
    }
    cout << specialPartitionPrefixSum(atoi(argv[1])) << "\n";
}
"""


def helperPath():
    digest = hashlib.sha256(HELPER_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_614_" + digest)


def compileHelper():
    binaryPath = helperPath()
    if os.path.exists(binaryPath):
        return binaryPath

    sourcePath = binaryPath + ".cpp"
    with open(sourcePath, "w", encoding="utf-8") as sourceFile:
        sourceFile.write(textwrap.dedent(HELPER_SOURCE).lstrip())

    command = ["c++", "-O3", "-std=c++17", sourcePath, "-o", binaryPath]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError("Problem 614 needs a local C++ compiler named 'c++'") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Problem 614 helper compilation failed:\n" + exc.stderr) from exc

    return binaryPath


def specialPartitionsUpTo(limit):
    partitions = [0] * (limit + 1)
    partitions[0] = 1

    for part in range(1, limit + 1):
        if part % 2 == 0 and part % 4 != 0:
            continue
        for total in range(limit, part - 1, -1):
            partitions[total] += partitions[total - part]

    return partitions


def specialPartitionCount(n):
    return specialPartitionsUpTo(n)[n]


def specialPartitionPrefixSum(limit):
    result = subprocess.run(
        [compileHelper(), str(limit)],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def runTests():
    partitions = specialPartitionsUpTo(1_000)
    assert partitions[1] == 1
    assert partitions[2] == 0
    assert partitions[3] == 1
    assert partitions[6] == 1
    assert partitions[10] == 3
    assert partitions[100] == 37_076
    assert partitions[1_000] == 3_699_177_285_485_660_336
    assert specialPartitionPrefixSum(1_000) == sum(partitions[1:]) % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = specialPartitionPrefixSum(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
