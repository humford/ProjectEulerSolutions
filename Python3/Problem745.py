import hashlib
import math
import os
import subprocess
import tempfile
import textwrap
import time


MODULUS = 1_000_000_007


HELPER_SOURCE = r"""
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <vector>

using namespace std;

static const long long MODULUS = 1000000007LL;

long long squareRoot(long long value) {
    long long root = sqrt((long double)value);
    while ((root + 1) * (root + 1) <= value) {
        ++root;
    }
    while (root * root > value) {
        --root;
    }
    return root;
}

long long largestSquareDivisorSum(long long limit) {
    int root = (int)squareRoot(limit);
    vector<long long> exactCounts(root + 1);
    long long total = 0;

    for (int divisor = root; divisor >= 1; --divisor) {
        long long count = limit / (1LL * divisor * divisor);
        for (int multiple = 2 * divisor; multiple <= root; multiple += divisor) {
            count -= exactCounts[multiple];
        }
        exactCounts[divisor] = count;

        long long square = 1LL * divisor * divisor % MODULUS;
        total = (total + square * (count % MODULUS)) % MODULUS;
    }

    return total;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        return 2;
    }
    cout << largestSquareDivisorSum(atoll(argv[1])) << "\n";
}
"""


def helperPath():
    digest = hashlib.sha256(HELPER_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_745_" + digest)


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
        raise RuntimeError("Problem 745 needs a local C++ compiler named 'c++'") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Problem 745 helper compilation failed:\n" + exc.stderr) from exc

    return binaryPath


def runHelper(limit):
    result = subprocess.run(
        [compileHelper(), str(limit)],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def largestSquareDivisor(n):
    best = 1
    for divisor in range(2, math.isqrt(n) + 1):
        square = divisor * divisor
        if n % square == 0:
            best = square
    return best


def bruteLargestSquareDivisorSum(limit):
    return sum(largestSquareDivisor(n) for n in range(1, limit + 1))


def largestSquareDivisorSum(limit):
    return runHelper(limit)


def runTests():
    assert largestSquareDivisor(18) == 9
    assert largestSquareDivisor(19) == 1
    assert bruteLargestSquareDivisorSum(10) == 24
    assert bruteLargestSquareDivisorSum(100) == 767
    assert largestSquareDivisorSum(10) == 24
    assert largestSquareDivisorSum(100) == 767


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestSquareDivisorSum(10 ** 14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
