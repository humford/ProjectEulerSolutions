import hashlib
import os
import subprocess
import tempfile
import time


CXX_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static const int BLOCK_SIZE = 64;

struct Node {
    int64_t sum;
    int64_t prefix;
    int64_t suffix;
    int64_t best;
};

static Node combine(const Node& left, const Node& right) {
    Node result;
    result.sum = left.sum + right.sum;
    result.prefix = std::max(left.prefix, left.sum + right.prefix);
    result.suffix = std::max(right.suffix, right.sum + left.suffix);
    result.best = std::max(
        std::max(left.best, right.best),
        left.suffix + right.prefix
    );
    return result;
}

class MaxSubarrayTracker {
public:
    explicit MaxSubarrayTracker(int length)
        : values((size_t)length, 0) {
        blockCount = (length + BLOCK_SIZE - 1) / BLOCK_SIZE;
        treeSize = 1;
        while (treeSize < blockCount) {
            treeSize <<= 1;
        }
        tree.assign((size_t)2 * treeSize, Node{0, 0, 0, 0});
    }

    void add(int position, int64_t delta) {
        values[(size_t)position] += delta;
        int block = position / BLOCK_SIZE;
        recomputeBlock(block);

        int node = treeSize + block;
        node >>= 1;
        while (node > 0) {
            tree[(size_t)node] =
                combine(tree[(size_t)2 * node], tree[(size_t)2 * node + 1]);
            node >>= 1;
        }
    }

    int64_t maxSubarraySum() const {
        return tree[1].best;
    }

private:
    std::vector<int64_t> values;
    std::vector<Node> tree;
    int blockCount;
    int treeSize;

    void recomputeBlock(int block) {
        int start = block * BLOCK_SIZE;
        int stop = std::min(start + BLOCK_SIZE, (int)values.size());

        int64_t sum = 0;
        int64_t prefix = 0;
        int64_t current = 0;
        int64_t best = 0;
        for (int index = start; index < stop; ++index) {
            int64_t value = values[(size_t)index];
            sum += value;
            prefix = std::max(prefix, sum);
            current = std::max<int64_t>(0, current + value);
            best = std::max(best, current);
        }

        int64_t suffix = 0;
        int64_t running = 0;
        for (int index = stop - 1; index >= start; --index) {
            running += values[(size_t)index];
            suffix = std::max(suffix, running);
        }

        tree[(size_t)treeSize + block] = Node{sum, prefix, suffix, best};
    }
};

static std::vector<int> tribonacciTerms(int count, int modulus) {
    std::vector<int> terms((size_t)count + 1, 0);
    if (count >= 2) {
        terms[2] = 1 % modulus;
    }
    for (int index = 3; index <= count; ++index) {
        terms[(size_t)index] =
            (
                (int64_t)terms[(size_t)index - 1]
                + terms[(size_t)index - 2]
                + terms[(size_t)index - 3]
            ) % modulus;
    }
    return terms;
}

static int64_t subarraySumDifference(
    int arrayLength,
    int upperSteps,
    int lowerSteps
) {
    std::vector<int> terms = tribonacciTerms(2 * upperSteps, arrayLength);
    MaxSubarrayTracker tracker(arrayLength);
    int64_t total = 0;

    for (int step = 1; step <= upperSteps; ++step) {
        int position = terms[(size_t)2 * step - 2];
        int valueTerm = terms[(size_t)2 * step - 1];
        int64_t delta = 2LL * valueTerm - arrayLength + 1LL;
        tracker.add(position, delta);

        if (step > lowerSteps) {
            total += tracker.maxSubarraySum();
        }
    }
    return total;
}

int main(int argc, char** argv) {
    if (argc != 4) {
        return 1;
    }

    int arrayLength = std::atoi(argv[1]);
    int upperSteps = std::atoi(argv[2]);
    int lowerSteps = std::atoi(argv[3]);
    std::cout << subarraySumDifference(arrayLength, upperSteps, lowerSteps)
              << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_663_" + digest)


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


def tribonacciTerms(count, modulus=None):
    terms = [0, 0, 1]
    while len(terms) <= count:
        value = terms[-1] + terms[-2] + terms[-3]
        if modulus is not None:
            value %= modulus
        terms.append(value)
    return terms


def maxSubarraySum(values):
    best = 0
    current = 0
    for value in values:
        current = max(0, current + value)
        best = max(best, current)
    return best


def subarraySumTotalDirect(arrayLength, steps):
    terms = tribonacciTerms(2 * steps, arrayLength)
    values = [0] * arrayLength
    total = 0
    for step in range(1, steps + 1):
        values[terms[2 * step - 2]] += (
            2 * terms[2 * step - 1] - arrayLength + 1
        )
        total += maxSubarraySum(values)
    return total


def subarraySumDifference(arrayLength, upperSteps, lowerSteps):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(arrayLength), str(upperSteps), str(lowerSteps)],
        text=True,
    )
    return int(output.strip())


def subarraySumTotal(arrayLength, steps):
    return subarraySumDifference(arrayLength, steps, 0)


def runTests():
    assert subarraySumTotalDirect(5, 6) == 32
    assert subarraySumTotal(5, 6) == 32
    assert subarraySumTotal(5, 100) == 2_416
    assert subarraySumTotal(14, 100) == 3_881
    assert subarraySumTotal(107, 1_000) == 1_618_572


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = subarraySumDifference(10_000_003, 10_200_000, 10_000_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
