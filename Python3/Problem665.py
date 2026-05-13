import hashlib
import os
import subprocess
import tempfile
import time


CXX_SOURCE = r"""
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

class SuccessorSet {
public:
    explicit SuccessorSet(int size)
        : parent((size_t)size + 1, 0) {
        for (int index = 0; index <= size; ++index) {
            parent[(size_t)index] = index;
        }
    }

    int find(int value) {
        int root = value;
        while (parent[(size_t)root] != root) {
            root = parent[(size_t)root];
        }
        while (parent[(size_t)value] != value) {
            int next = parent[(size_t)value];
            parent[(size_t)value] = root;
            value = next;
        }
        return root;
    }

    bool used(int value) const {
        return parent[(size_t)value] != value;
    }

    void mark(int value) {
        if (parent[(size_t)value] == value) {
            parent[(size_t)value] = find(value + 1);
        }
    }

private:
    std::vector<int> parent;
};

static int64_t losingPositionSum(int limit) {
    int halfLimit = limit / 2;
    int maxCoordinate = (int)(1.25 * limit) + 100;

    SuccessorSet coordinates(maxCoordinate + 1);
    SuccessorSet differences(maxCoordinate + 1);

    int invariantMinimum = -2 * maxCoordinate;
    int invariantOffset = -invariantMinimum;
    int invariantLength = 3 * maxCoordinate + 1;
    SuccessorSet invariants(invariantLength + 1);

    auto invariantIndex = [invariantOffset](int value) {
        return value + invariantOffset;
    };

    coordinates.mark(0);
    differences.mark(0);
    invariants.mark(invariantIndex(0));

    int64_t total = 0;
    int first = 1;
    while (true) {
        first = coordinates.find(first);
        if (first > halfLimit) {
            break;
        }

        int second = first + 1;
        while (true) {
            second = coordinates.find(second);

            int difference = second - first;
            if (differences.used(difference)) {
                int nextDifference = differences.find(difference);
                second = first + nextDifference;
                continue;
            }

            int invariantForward = second - 2 * first;
            int forwardIndex = invariantIndex(invariantForward);
            if (invariants.used(forwardIndex)) {
                int nextIndex = invariants.find(forwardIndex);
                if (nextIndex >= invariantLength) {
                    std::cerr << "invariant range too small\n";
                    std::exit(2);
                }
                second = 2 * first + (nextIndex - invariantOffset);
                continue;
            }

            int invariantReverse = first - 2 * second;
            int reverseIndex = invariantIndex(invariantReverse);
            if (invariants.used(reverseIndex)) {
                ++second;
                continue;
            }

            break;
        }

        coordinates.mark(first);
        coordinates.mark(second);
        differences.mark(second - first);
        invariants.mark(invariantIndex(second - 2 * first));
        invariants.mark(invariantIndex(first - 2 * second));

        int sum = first + second;
        if (sum <= limit) {
            total += sum;
        }
        ++first;
    }

    return total;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        return 1;
    }

    int limit = std::atoi(argv[1]);
    std::cout << losingPositionSum(limit) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_665_" + digest)


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


def losingPositionSum(limit):
    binaryPath = compileHelper()
    output = subprocess.check_output([binaryPath, str(limit)], text=True)
    return int(output.strip())


def runTests():
    assert losingPositionSum(10) == 21
    assert losingPositionSum(100) == 1_164
    assert losingPositionSum(1_000) == 117_002


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = losingPositionSum(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
