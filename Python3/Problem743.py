import hashlib
import os
import subprocess
import tempfile
import textwrap
import time


MODULUS = 1_000_000_007


HELPER_SOURCE = r"""
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using namespace std;

static const long long MODULUS = 1000000007LL;

long long modularPower(long long base, long long exponent) {
    long long result = 1;
    base %= MODULUS;
    while (exponent > 0) {
        if (exponent & 1LL) {
            result = result * base % MODULUS;
        }
        base = base * base % MODULUS;
        exponent >>= 1LL;
    }
    return result;
}

int repeatedPeriodCoefficient(long long periodLength, long long repeatCount) {
    int half = (int)(periodLength / 2);
    vector<uint32_t> inverses(half + 1);
    if (half >= 1) {
        inverses[1] = 1;
    }
    for (int value = 2; value <= half; ++value) {
        inverses[value] =
            (uint32_t)(MODULUS - (MODULUS / value) * 1LL * inverses[MODULUS % value] % MODULUS);
    }

    long long oneSumColumnChoices = modularPower(2, repeatCount);
    long long term = modularPower(oneSumColumnChoices, periodLength);
    long long inverseChoiceSquare =
        modularPower(oneSumColumnChoices * oneSumColumnChoices % MODULUS, MODULUS - 2);
    long long total = term;

    for (int pairs = 0; pairs < half; ++pairs) {
        long long remaining = periodLength - 2LL * pairs;
        long long inverse = inverses[pairs + 1];
        term = term * (remaining % MODULUS) % MODULUS;
        term = term * ((remaining - 1) % MODULUS) % MODULUS;
        term = term * inverse % MODULUS * inverse % MODULUS;
        term = term * inverseChoiceSquare % MODULUS;
        total += term;
        if (total >= MODULUS) {
            total -= MODULUS;
        }
    }

    return (int)total;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 2;
    }
    long long periodLength = atoll(argv[1]);
    long long repeatCount = atoll(argv[2]);
    cout << repeatedPeriodCoefficient(periodLength, repeatCount) << "\n";
}
"""


def helperPath():
    digest = hashlib.sha256(HELPER_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_743_" + digest)


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
        raise RuntimeError("Problem 743 needs a local C++ compiler named 'c++'") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Problem 743 helper compilation failed:\n" + exc.stderr) from exc

    return binaryPath


def runHelper(periodLength, repeatCount):
    result = subprocess.run(
        [compileHelper(), str(periodLength), str(repeatCount)],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return int(result.stdout.strip())


def exactWindowMatrixCount(k, n):
    baseColumns = n // k
    extraColumns = n % k
    coefficients = [0] * (k + 1)
    coefficients[0] = 1

    for residue in range(k):
        oneSumColumnChoices = 2 ** (baseColumns + (1 if residue < extraColumns else 0))
        nextCoefficients = [0] * (k + 1)
        for degree, value in enumerate(coefficients):
            if value == 0:
                continue
            nextCoefficients[degree] += value
            if degree + 1 <= k:
                nextCoefficients[degree + 1] += value * oneSumColumnChoices
            if degree + 2 <= k:
                nextCoefficients[degree + 2] += value
        coefficients = nextCoefficients

    return coefficients[k]


def windowMatrixCountModulo(k, n):
    if n % k != 0:
        return exactWindowMatrixCount(k, n) % MODULUS
    return runHelper(k, n // k)


def runTests():
    assert exactWindowMatrixCount(3, 9) == 560
    assert exactWindowMatrixCount(4, 20) == 1_060_870
    assert windowMatrixCountModulo(3, 9) == 560
    assert windowMatrixCountModulo(4, 20) == 1_060_870


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = windowMatrixCountModulo(10 ** 8, 10 ** 16)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
