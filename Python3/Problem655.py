import hashlib
import os
import subprocess
import tempfile
import time


CXX_SOURCE = r"""
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static int divisorValue;

static std::vector<std::array<int, 10>> digitContributions(
    const std::vector<int>& coefficients
) {
    std::vector<std::array<int, 10>> contributions(coefficients.size());
    for (int index = 0; index < (int)coefficients.size(); ++index) {
        for (int digit = 0; digit <= 9; ++digit) {
            contributions[(size_t)index][(size_t)digit] =
                (int)((int64_t)digit * coefficients[(size_t)index]
                      % divisorValue);
        }
    }
    return contributions;
}

static void addRightResidues(
    const std::vector<std::array<int, 10>>& contributions,
    int index,
    int end,
    int residue,
    std::vector<uint32_t>& counts
) {
    if (index == end) {
        ++counts[(size_t)residue];
        return;
    }

    const std::array<int, 10>& options = contributions[(size_t)index];
    for (int digit = 0; digit <= 9; ++digit) {
        int next = residue + options[(size_t)digit];
        if (next >= divisorValue) {
            next -= divisorValue;
        }
        addRightResidues(contributions, index + 1, end, next, counts);
    }
}

static uint64_t countLeftMatches(
    const std::vector<std::array<int, 10>>& contributions,
    int index,
    int end,
    int residue,
    const std::vector<uint32_t>& rightCounts
) {
    if (index == end) {
        int complement = residue == 0 ? 0 : divisorValue - residue;
        return rightCounts[(size_t)complement];
    }

    uint64_t total = 0;
    const std::array<int, 10>& options = contributions[(size_t)index];
    int firstDigit = index == 0 ? 1 : 0;
    for (int digit = firstDigit; digit <= 9; ++digit) {
        int next = residue + options[(size_t)digit];
        if (next >= divisorValue) {
            next -= divisorValue;
        }
        total += countLeftMatches(contributions, index + 1, end, next, rightCounts);
    }
    return total;
}

static std::vector<int> palindromeCoefficients(int length) {
    std::vector<int> powers((size_t)length, 1);
    for (int index = 1; index < length; ++index) {
        powers[(size_t)index] = (int)((int64_t)powers[(size_t)index - 1] * 10
                                      % divisorValue);
    }

    int halfLength = (length + 1) / 2;
    std::vector<int> coefficients((size_t)halfLength, 0);
    for (int index = 0; index < halfLength; ++index) {
        int leftPower = length - 1 - index;
        int rightPower = index;
        int coefficient = powers[(size_t)leftPower];
        if (leftPower != rightPower) {
            coefficient += powers[(size_t)rightPower];
            if (coefficient >= divisorValue) {
                coefficient -= divisorValue;
            }
        }
        coefficients[(size_t)index] = coefficient;
    }
    return coefficients;
}

static uint64_t divisiblePalindromeCountForLength(int length) {
    std::vector<int> coefficients = palindromeCoefficients(length);
    std::vector<std::array<int, 10>> contributions =
        digitContributions(coefficients);

    int halfLength = (int)coefficients.size();
    int leftLength = (halfLength + 1) / 2;
    std::vector<uint32_t> rightCounts((size_t)divisorValue, 0);
    addRightResidues(contributions, leftLength, halfLength, 0, rightCounts);
    return countLeftMatches(contributions, 0, leftLength, 0, rightCounts);
}

static uint64_t divisiblePalindromeCountBelowPowerOfTen(
    int divisor,
    int exponent
) {
    divisorValue = divisor;
    uint64_t total = 0;
    for (int length = 1; length <= exponent; ++length) {
        total += divisiblePalindromeCountForLength(length);
    }
    return total;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 1;
    }

    int divisor = std::atoi(argv[1]);
    int exponent = std::atoi(argv[2]);
    std::cout << divisiblePalindromeCountBelowPowerOfTen(divisor, exponent)
              << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_655_" + digest)


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
    )
    return binaryPath


def generatePalindromesBelow(limit):
    palindromes = []
    digits = len(str(limit - 1))
    for length in range(1, digits + 1):
        halfLength = (length + 1) // 2
        start = 1
        if length > 1:
            start = 10 ** (halfLength - 1)
        stop = 10 ** halfLength
        for firstHalf in range(start, stop):
            text = str(firstHalf)
            palindrome = int(text + text[-(1 if length % 2 else 0) - 1 :: -1])
            if palindrome < limit:
                palindromes.append(palindrome)
    return palindromes


def bruteDivisiblePalindromeCount(divisor, limit):
    return sum(
        1
        for palindrome in generatePalindromesBelow(limit)
        if palindrome % divisor == 0
    )


def divisiblePalindromeCountBelowPowerOfTen(divisor, exponent):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(divisor), str(exponent)],
        text=True,
    )
    return int(output.strip())


def runTests():
    first = [
        palindrome
        for palindrome in generatePalindromesBelow(20_000)
        if palindrome % 109 == 0
    ][:3]
    assert first == [545, 5_995, 15_151]
    assert bruteDivisiblePalindromeCount(109, 100_000) == 9
    assert divisiblePalindromeCountBelowPowerOfTen(109, 5) == 9

    for divisor, exponent in [(7, 4), (37, 5), (109, 5)]:
        assert divisiblePalindromeCountBelowPowerOfTen(
            divisor,
            exponent,
        ) == bruteDivisiblePalindromeCount(divisor, 10 ** exponent)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = divisiblePalindromeCountBelowPowerOfTen(10_000_019, 32)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
