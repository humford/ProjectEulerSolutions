import hashlib
import itertools
import os
import subprocess
import tempfile
import time


MODULUS = 1_000_000_007


CXX_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <unordered_map>
#include <vector>

static const int MODULUS = 1000000007;

static int inversionBudget;
static int cappedDeficit;

struct State {
    std::vector<unsigned char> suffix;
    signed char baseMaxDeficit;
    signed char basePairSecondDeficit;

    bool operator==(const State& other) const {
        return suffix == other.suffix
            && baseMaxDeficit == other.baseMaxDeficit
            && basePairSecondDeficit == other.basePairSecondDeficit;
    }
};

struct StateHash {
    size_t operator()(const State& state) const {
        uint64_t hash = 1469598103934665603ULL;
        auto mix = [&](unsigned char value) {
            hash ^= value;
            hash *= 1099511628211ULL;
        };

        mix((unsigned char)state.suffix.size());
        mix((unsigned char)(state.baseMaxDeficit + 1));
        mix((unsigned char)(state.basePairSecondDeficit + 1));
        for (unsigned char value : state.suffix) {
            mix(value);
        }
        return (size_t)hash;
    }
};

static unsigned char shiftDeficit(unsigned char value) {
    return (unsigned char)std::min(cappedDeficit, (int)value + 1);
}

static signed char shiftSummary(signed char value) {
    if (value < 0) {
        return -1;
    }
    return (signed char)std::min(cappedDeficit, (int)value + 1);
}

static void updateSummary(
    signed char& maxDeficit,
    signed char& pairSecondDeficit,
    unsigned char valueDeficit
) {
    if (maxDeficit >= 0 && maxDeficit > (signed char)valueDeficit) {
        pairSecondDeficit =
            std::max(pairSecondDeficit, (signed char)valueDeficit);
    }
    maxDeficit = std::max(maxDeficit, (signed char)valueDeficit);
}

static void buildCutData(
    const State& state,
    std::vector<signed char>& pairBefore,
    std::vector<unsigned char>& minAfter
) {
    int suffixLength = (int)state.suffix.size();
    pairBefore.assign((size_t)suffixLength + 1, -1);
    minAfter.assign((size_t)suffixLength + 1, cappedDeficit + 1);

    signed char maxDeficit = state.baseMaxDeficit;
    signed char pairSecondDeficit = state.basePairSecondDeficit;
    pairBefore[(size_t)suffixLength] = pairSecondDeficit;
    for (int used = 1; used <= suffixLength; ++used) {
        updateSummary(
            maxDeficit,
            pairSecondDeficit,
            state.suffix[(size_t)used - 1]
        );
        pairBefore[(size_t)(suffixLength - used)] = pairSecondDeficit;
    }

    unsigned char runningMinimum = cappedDeficit + 1;
    minAfter[0] = cappedDeficit + 1;
    for (int after = 1; after <= suffixLength; ++after) {
        runningMinimum =
            std::min(
                runningMinimum,
                state.suffix[(size_t)(suffixLength - after)]
            );
        minAfter[(size_t)after] = runningMinimum;
    }
}

static State transitionState(
    const State& state,
    int after,
    int remainingAfter
) {
    std::vector<unsigned char> shiftedSuffix;
    shiftedSuffix.reserve(state.suffix.size() + 1);
    for (unsigned char value : state.suffix) {
        shiftedSuffix.push_back(shiftDeficit(value));
    }

    signed char shiftedBaseMax = shiftSummary(state.baseMaxDeficit);
    signed char shiftedBasePair = shiftSummary(state.basePairSecondDeficit);

    int suffixLength = (int)shiftedSuffix.size();
    std::vector<unsigned char> fullTail;
    fullTail.reserve((size_t)suffixLength + 1);
    fullTail.insert(
        fullTail.end(),
        shiftedSuffix.begin(),
        shiftedSuffix.begin() + (suffixLength - after)
    );
    fullTail.push_back(0);
    fullTail.insert(
        fullTail.end(),
        shiftedSuffix.begin() + (suffixLength - after),
        shiftedSuffix.end()
    );

    int keep = std::min(remainingAfter, (int)fullTail.size());
    int drop = (int)fullTail.size() - keep;
    signed char newBaseMax = shiftedBaseMax;
    signed char newBasePair = shiftedBasePair;

    if (drop == 0) {
        newBaseMax = -1;
        newBasePair = -1;
    } else {
        for (int index = 0; index < drop; ++index) {
            updateSummary(newBaseMax, newBasePair, fullTail[(size_t)index]);
        }
    }

    State result;
    result.baseMaxDeficit = newBaseMax;
    result.basePairSecondDeficit = newBasePair;
    result.suffix.assign(fullTail.end() - keep, fullTail.end());
    return result;
}

static int constrainedPermutationCount(long long maxLength, int maxInversions) {
    inversionBudget = maxInversions;
    cappedDeficit = maxInversions + 2;

    std::vector<std::unordered_map<State, int, StateHash>> states(
        (size_t)maxInversions + 1
    );

    State empty;
    empty.baseMaxDeficit = -1;
    empty.basePairSecondDeficit = -1;
    states[0][empty] = 1;

    long long cumulative = 1;
    long long previousExact = -1;
    int stableSteps = 0;

    for (long long length = 0; length < maxLength; ++length) {
        std::vector<std::unordered_map<State, int, StateHash>> nextStates(
            (size_t)maxInversions + 1
        );

        for (int used = 0; used <= maxInversions; ++used) {
            int remaining = maxInversions - used;
            for (const auto& entry : states[(size_t)used]) {
                const State& state = entry.first;
                int count = entry.second;

                std::vector<signed char> pairBefore;
                std::vector<unsigned char> minAfter;
                buildCutData(state, pairBefore, minAfter);

                int maxAfter =
                    std::min(
                        {
                            remaining,
                            (int)length,
                            (int)state.suffix.size()
                        }
                    );
                for (int after = 0; after <= maxAfter; ++after) {
                    if (
                        after > 0
                        && pairBefore[(size_t)after] >= 0
                        && minAfter[(size_t)after]
                            < (unsigned char)pairBefore[(size_t)after]
                    ) {
                        continue;
                    }

                    State target =
                        transitionState(state, after, remaining - after);
                    int& slot = nextStates[(size_t)(used + after)][target];
                    slot += count;
                    if (slot >= MODULUS) {
                        slot -= MODULUS;
                    }
                }
            }
        }

        states.swap(nextStates);

        long long exact = 0;
        size_t stateCount = 0;
        for (int used = 0; used <= maxInversions; ++used) {
            stateCount += states[(size_t)used].size();
            for (const auto& entry : states[(size_t)used]) {
                exact += entry.second;
                exact %= MODULUS;
            }
        }

        cumulative += exact;
        cumulative %= MODULUS;

        long long currentLength = length + 1;
        if (exact == previousExact) {
            stableSteps += 1;
        } else {
            stableSteps = 0;
            previousExact = exact;
        }

        if (
            currentLength < maxLength
            && currentLength >= maxInversions + 1
            && stableSteps >= 3
            && stateCount == (size_t)maxInversions + 1
        ) {
            long long remainingLengths =
                (maxLength - currentLength) % MODULUS;
            cumulative =
                (
                    cumulative
                    + remainingLengths * (exact % MODULUS)
                ) % MODULUS;
            break;
        }
    }

    return (int)cumulative;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        return 1;
    }

    long long maxLength = std::atoll(argv[1]);
    int maxInversions = std::atoi(argv[2]);
    std::cout << constrainedPermutationCount(maxLength, maxInversions) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_631_" + digest)


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


def inversionCount(permutation):
    return sum(
        1
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
        if permutation[i] > permutation[j]
    )


def hasPattern1243(permutation):
    length = len(permutation)
    for indices in itertools.combinations(range(length), 4):
        values = [permutation[index] for index in indices]
        order = {value: rank + 1 for rank, value in enumerate(sorted(values))}
        if tuple(order[value] for value in values) == (1, 2, 4, 3):
            return True
    return False


def constrainedPermutationCountBrute(maxLength, maxInversions):
    count = 1
    for length in range(1, maxLength + 1):
        for permutation in itertools.permutations(range(1, length + 1)):
            if (
                inversionCount(permutation) <= maxInversions
                and not hasPattern1243(permutation)
            ):
                count += 1
    return count


def constrainedPermutationCount(maxLength, maxInversions):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(maxLength), str(maxInversions)],
        text=True,
    )
    return int(output.strip())


def runTests():
    assert constrainedPermutationCountBrute(2, 0) == 3
    assert constrainedPermutationCount(2, 0) == 3
    assert constrainedPermutationCount(4, 5) == 32
    assert constrainedPermutationCount(10, 25) == 294_400


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = constrainedPermutationCount(10 ** 18, 40) % MODULUS
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
