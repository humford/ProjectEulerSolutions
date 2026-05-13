import hashlib
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


CXX_SOURCE = r"""
#include <cstdlib>
#include <iostream>
#include <vector>

static const long long MODULUS = 1000000007LL;

static long long modPow(long long base, long long exponent) {
    long long result = 1;
    while (exponent > 0) {
        if (exponent & 1) {
            result = result * base % MODULUS;
        }
        base = base * base % MODULUS;
        exponent >>= 1;
    }
    return result;
}

static std::vector<long long> generateTerms(int maxValue, int termCount) {
    int dimension = maxValue - 1;
    std::vector<long long> counts((size_t)dimension, 1);
    std::vector<long long> terms;
    terms.reserve((size_t)termCount);

    for (int term = 0; term < termCount; ++term) {
        long long total = 0;
        for (long long value : counts) {
            total += value;
            if (total >= MODULUS) {
                total -= MODULUS;
            }
        }
        terms.push_back(total);

        std::vector<long long> prefix((size_t)dimension + 1, 0);
        for (int index = 0; index < dimension; ++index) {
            prefix[(size_t)index + 1] =
                (prefix[(size_t)index] + counts[(size_t)index]) % MODULUS;
        }

        std::vector<long long> next((size_t)dimension, 0);
        for (int index = 0; index < dimension; ++index) {
            next[(size_t)index] = prefix[(size_t)(dimension - index)];
        }
        counts.swap(next);
    }

    return terms;
}

static std::vector<long long> berlekampMassey(const std::vector<long long>& sequence) {
    std::vector<long long> current(1, 1);
    std::vector<long long> previous(1, 1);
    int length = 0;
    int shift = 1;
    long long discrepancyBase = 1;

    for (int index = 0; index < (int)sequence.size(); ++index) {
        long long discrepancy = sequence[(size_t)index];
        for (int offset = 1; offset <= length; ++offset) {
            discrepancy =
                (
                    discrepancy
                    + current[(size_t)offset]
                    * sequence[(size_t)(index - offset)]
                ) % MODULUS;
        }

        if (discrepancy == 0) {
            ++shift;
            continue;
        }

        std::vector<long long> saved = current;
        long long scale =
            discrepancy * modPow(discrepancyBase, MODULUS - 2) % MODULUS;
        if (current.size() < previous.size() + (size_t)shift) {
            current.resize(previous.size() + (size_t)shift, 0);
        }
        for (int previousIndex = 0;
             previousIndex < (int)previous.size();
             ++previousIndex) {
            current[(size_t)(previousIndex + shift)] =
                (
                    current[(size_t)(previousIndex + shift)]
                    - scale * previous[(size_t)previousIndex]
                ) % MODULUS;
            if (current[(size_t)(previousIndex + shift)] < 0) {
                current[(size_t)(previousIndex + shift)] += MODULUS;
            }
        }

        if (2 * length <= index) {
            length = index + 1 - length;
            previous = saved;
            discrepancyBase = discrepancy;
            shift = 1;
        } else {
            ++shift;
        }
    }

    std::vector<long long> recurrence((size_t)length, 0);
    for (int index = 0; index < length; ++index) {
        recurrence[(size_t)index] =
            (MODULUS - current[(size_t)index + 1]) % MODULUS;
    }
    return recurrence;
}

static std::vector<long long> combinePolynomials(
    const std::vector<long long>& left,
    const std::vector<long long>& right,
    const std::vector<long long>& recurrence
) {
    int order = (int)recurrence.size();
    std::vector<long long> product((size_t)2 * order - 1, 0);
    for (int i = 0; i < order; ++i) {
        if (left[(size_t)i] == 0) {
            continue;
        }
        for (int j = 0; j < order; ++j) {
            product[(size_t)(i + j)] =
                (
                    product[(size_t)(i + j)]
                    + left[(size_t)i] * right[(size_t)j]
                ) % MODULUS;
        }
    }

    for (int degree = 2 * order - 2; degree >= order; --degree) {
        long long coefficient = product[(size_t)degree];
        if (coefficient == 0) {
            continue;
        }
        for (int offset = 1; offset <= order; ++offset) {
            product[(size_t)(degree - offset)] =
                (
                    product[(size_t)(degree - offset)]
                    + coefficient * recurrence[(size_t)offset - 1]
                ) % MODULUS;
        }
    }

    product.resize((size_t)order);
    return product;
}

static long long linearRecurrenceValue(
    const std::vector<long long>& initialTerms,
    const std::vector<long long>& recurrence,
    long long index
) {
    int order = (int)recurrence.size();
    if (index < order) {
        return initialTerms[(size_t)index];
    }

    std::vector<long long> result((size_t)order, 0);
    result[0] = 1;
    std::vector<long long> base((size_t)order, 0);
    if (order == 1) {
        base[0] = recurrence[0];
    } else {
        base[1] = 1;
    }

    while (index > 0) {
        if (index & 1) {
            result = combinePolynomials(result, base, recurrence);
        }
        base = combinePolynomials(base, base, recurrence);
        index >>= 1;
    }

    long long answer = 0;
    for (int index = 0; index < order; ++index) {
        answer =
            (
                answer
                + result[(size_t)index] * initialTerms[(size_t)index]
            ) % MODULUS;
    }
    return answer;
}

static long long neighbourlyTupleCount(int maxValue, long long length) {
    int order = maxValue - 1;
    std::vector<long long> terms = generateTerms(maxValue, 2 * order + 10);
    std::vector<long long> recurrence = berlekampMassey(terms);
    terms.resize(recurrence.size());
    return linearRecurrenceValue(terms, recurrence, length - 1);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 1;
    }

    int maxValue = std::atoi(argv[1]);
    long long length = std::atoll(argv[2]);
    std::cout << neighbourlyTupleCount(maxValue, length) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_654_" + digest)


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


def neighbourlyTupleCountDirect(maxValue, length):
    counts = [1] * maxValue
    for _ in range(length - 1):
        prefix = [0]
        for value in counts:
            prefix.append((prefix[-1] + value) % MODULUS)
        counts = [
            prefix[maxValue - value]
            for value in range(1, maxValue + 1)
        ]
    return sum(counts) % MODULUS


def neighbourlyTupleCount(maxValue, length):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(maxValue), str(length)],
        text=True,
    )
    return int(output.strip())


def runTests():
    assert neighbourlyTupleCountDirect(3, 4) == 8
    assert neighbourlyTupleCount(3, 4) == 8
    assert neighbourlyTupleCount(5, 5) == 246
    assert neighbourlyTupleCount(10, 10 ** 2) == 862_820_094
    assert neighbourlyTupleCount(10 ** 2, 10) == 782_136_797


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = neighbourlyTupleCount(5_000, 10 ** 12) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
