import hashlib
import math
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


CXX_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static const uint32_t MODULUS = 1000000007U;

struct Step {
    int dx;
    int dy;
};

static std::vector<int> fibonacciNumbersUpTo(int limit) {
    std::vector<int> numbers;
    numbers.push_back(1);
    numbers.push_back(2);
    while (numbers.back() <= limit) {
        int size = (int)numbers.size();
        numbers.push_back(numbers[(size_t)size - 1] + numbers[(size_t)size - 2]);
    }
    return numbers;
}

static std::vector<Step> fibonacciSteps(int width, int height) {
    int distanceLimit = 1;
    while ((int64_t)distanceLimit * distanceLimit
           < (int64_t)width * width + (int64_t)height * height) {
        ++distanceLimit;
    }

    std::vector<Step> steps;
    for (int number : fibonacciNumbersUpTo(distanceLimit + 1)) {
        int64_t square = (int64_t)number * number;
        for (int dx = 0; dx <= width && (int64_t)dx * dx <= square; ++dx) {
            int64_t dySquare = square - (int64_t)dx * dx;
            int dy = (int)std::llround(std::sqrt((long double)dySquare));
            if ((int64_t)dy * dy == dySquare
                && dy <= height
                && (dx != 0 || dy != 0)) {
                steps.push_back({dx, dy});
            }
        }
    }

    std::sort(
        steps.begin(),
        steps.end(),
        [](const Step& left, const Step& right) {
            if (left.dx != right.dx) {
                return left.dx < right.dx;
            }
            return left.dy < right.dy;
        }
    );
    return steps;
}

static uint32_t fibonacciPathCount(int width, int height) {
    std::vector<Step> steps = fibonacciSteps(width, height);
    int stride = height + 1;
    std::vector<uint32_t> counts((size_t)(width + 1) * stride, 0);
    counts[0] = 1;

    for (int x = 0; x <= width; ++x) {
        size_t rowOffset = (size_t)x * stride;
        for (int y = 0; y <= height; ++y) {
            if (x == 0 && y == 0) {
                continue;
            }

            uint64_t total = 0;
            for (const Step& step : steps) {
                if (step.dx > x) {
                    break;
                }
                if (step.dy <= y) {
                    total += counts[(size_t)(x - step.dx) * stride + y - step.dy];
                }
            }
            counts[rowOffset + y] = (uint32_t)(total % MODULUS);
        }
    }

    return counts[(size_t)width * stride + height];
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 1;
    }

    int width = std::atoi(argv[1]);
    int height = std::atoi(argv[2]);
    std::cout << fibonacciPathCount(width, height) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_662_" + digest)


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


def fibonacciNumbersUpTo(limit):
    numbers = [1, 2]
    while numbers[-1] <= limit:
        numbers.append(numbers[-1] + numbers[-2])
    return numbers


def fibonacciSteps(width, height):
    distanceLimit = math.isqrt(width * width + height * height) + 1
    fibonacciSquares = {
        number * number
        for number in fibonacciNumbersUpTo(distanceLimit + 1)
    }
    steps = []
    for dx in range(width + 1):
        for dy in range(height + 1):
            if (dx or dy) and dx * dx + dy * dy in fibonacciSquares:
                steps.append((dx, dy))
    return steps


def fibonacciPathCountDirect(width, height):
    steps = fibonacciSteps(width, height)
    counts = [[0] * (height + 1) for _ in range(width + 1)]
    counts[0][0] = 1
    for x in range(width + 1):
        for y in range(height + 1):
            if x == 0 and y == 0:
                continue
            counts[x][y] = sum(
                counts[x - dx][y - dy]
                for dx, dy in steps
                if x >= dx and y >= dy
            ) % MODULUS
    return counts[width][height]


def fibonacciPathCount(width, height):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(width), str(height)],
        text=True,
    )
    return int(output.strip())


def runTests():
    assert fibonacciPathCountDirect(3, 4) == 278
    assert fibonacciPathCount(3, 4) == 278
    assert fibonacciPathCount(10, 10) == 215_846_462


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciPathCount(10_000, 10_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
