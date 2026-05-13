import hashlib
import os
import subprocess
import tempfile
import textwrap
import time


HELPER_SOURCE = r"""
#include <array>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>

using namespace std;

struct Triple {
    long long p;
    long long q;
    long long r;
};

static inline Triple inverseTransform(int index, long long p, long long q, long long r) {
    if (index == 0) {
        return {-2 * p - q + 2 * r, p + 2 * q - 2 * r, -2 * p - 2 * q + 3 * r};
    }
    if (index == 1) {
        return {p + 2 * q - 2 * r, -2 * p - q + 2 * r, -2 * p - 2 * q + 3 * r};
    }
    return {2 * p + q - 2 * r, p + 2 * q - 2 * r, -2 * p - 2 * q + 3 * r};
}

static inline bool isRoot(long long p, long long q, long long r) {
    for (int index = 0; index < 3; ++index) {
        Triple parent = inverseTransform(index, p, q, r);
        if (parent.p > 0 && parent.q > 0 && parent.r > 0
            && parent.p <= parent.q && parent.q <= parent.r) {
            return false;
        }
    }
    return true;
}

vector<vector<Triple>> generateRoots(int maxShift) {
    int maxR = (5 * maxShift + 1) / 2 + 10;
    vector<vector<Triple>> roots(maxShift + 1);
    if (maxShift >= 0) {
        roots[0].push_back({3, 4, 5});
    }

    for (int r = 1; r <= maxR; ++r) {
        long long rr = 1LL * r * r;
        for (int p = 1; p <= r; ++p) {
            long long pp = 1LL * p * p;
            for (int q = p; q <= r; ++q) {
                long long shift = rr - pp - 1LL * q * q;
                if (shift < 1 || shift > maxShift) {
                    continue;
                }
                if (std::gcd(p, std::gcd(q, r)) == 1 && isRoot(p, q, r)) {
                    roots[(int)shift].push_back({p, q, r});
                }
            }
        }
    }

    return roots;
}

static inline array<Triple, 3> children(Triple triple) {
    long long p = triple.p;
    long long q = triple.q;
    long long r = triple.r;
    return {
        Triple{-2 * p + q + 2 * r, -p + 2 * q + 2 * r, -2 * p + 2 * q + 3 * r},
        Triple{p - 2 * q + 2 * r, 2 * p - q + 2 * r, 2 * p - 2 * q + 3 * r},
        Triple{2 * p + q + 2 * r, p + 2 * q + 2 * r, 2 * p + 2 * q + 3 * r},
    };
}

long long countFromRoots(long long limit, const vector<Triple>& roots) {
    long long count = 0;
    vector<Triple> stack = roots;

    while (!stack.empty()) {
        Triple triple = stack.back();
        stack.pop_back();

        if (triple.p + triple.q + triple.r > limit) {
            continue;
        }
        ++count;

        array<Triple, 3> next = children(triple);
        for (int index = 0; index < 3; ++index) {
            bool duplicate = false;
            for (int previous = 0; previous < index; ++previous) {
                if (next[index].p == next[previous].p
                    && next[index].q == next[previous].q
                    && next[index].r == next[previous].r) {
                    duplicate = true;
                    break;
                }
            }
            if (!duplicate && next[index].p + next[index].q + next[index].r <= limit) {
                stack.push_back(next[index]);
            }
        }
    }

    return count;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        return 2;
    }

    int maxShift = atoi(argv[1]);
    long long limit = atoll(argv[2]);
    int singleShift = -1;
    if (argc >= 4) {
        singleShift = atoi(argv[3]);
        if (singleShift > maxShift) {
            maxShift = singleShift;
        }
    }

    vector<vector<Triple>> roots = generateRoots(maxShift);
    if (singleShift >= 0) {
        cout << countFromRoots(limit, roots[singleShift]) << "\n";
        return 0;
    }

    long long total = 0;
    for (int shift = 0; shift <= maxShift; ++shift) {
        total += countFromRoots(limit, roots[shift]);
    }
    cout << total << "\n";
}
"""


def helperPath():
    digest = hashlib.sha256(HELPER_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_730_" + digest)


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
        raise RuntimeError("Problem 730 needs a local C++ compiler named 'c++'") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Problem 730 helper compilation failed:\n" + exc.stderr) from exc

    return binaryPath


def runHelper(maxShift, limit, singleShift=None):
    command = [compileHelper(), str(maxShift), str(limit)]
    if singleShift is not None:
        command.append(str(singleShift))

    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)
    return int(result.stdout.strip())


def shiftedPrimitiveTripleCount(shift, limit):
    return runHelper(shift, limit, singleShift=shift)


def shiftedPrimitiveTripleSum(maxShift, limit):
    return runHelper(maxShift, limit)


def runTests():
    assert shiftedPrimitiveTripleCount(0, 10**4) == 703
    assert shiftedPrimitiveTripleCount(20, 10**4) == 1_979
    assert shiftedPrimitiveTripleSum(10, 10**4) == 10_956


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = shiftedPrimitiveTripleSum(10**2, 10**8)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
