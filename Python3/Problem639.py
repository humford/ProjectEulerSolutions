import hashlib
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

static const long long MODULUS = 1000000007LL;

class SummatoryRadicalPowers {
public:
    explicit SummatoryRadicalPowers(long long limit)
        : limit(limit), root((int)std::sqrt((long double)limit) + 3) {
        buildPrimes();
        buildQuotients();
    }

    int solveExponent(int exponent) {
        this->exponent = exponent;
        buildPowerSumInterpolation();
        buildPrimePowerSums();
        return sumFromPrimeIndex(limit, 0);
    }

private:
    long long limit;
    int root;
    int exponent;
    std::vector<int> primes;
    std::vector<long long> quotients;
    std::vector<int> idSmall;
    std::vector<int> idLarge;
    std::vector<int> primePowers;
    std::vector<int> primePowerPrefix;
    std::vector<int> powerSumPrefix;
    std::vector<int> inverseFactorials;
    std::vector<int> primePowerSums;

    static int normalize(long long value) {
        value %= MODULUS;
        if (value < 0) {
            value += MODULUS;
        }
        return (int)value;
    }

    static long long modularPower(long long base, long long exponent) {
        long long result = 1;
        base %= MODULUS;
        while (exponent > 0) {
            if (exponent & 1) {
                result = (long long)((__int128)result * base % MODULUS);
            }
            base = (long long)((__int128)base * base % MODULUS);
            exponent >>= 1;
        }
        return result;
    }

    void buildPrimes() {
        std::vector<char> isComposite((size_t)root + 1, 0);
        for (int number = 2; number <= root; ++number) {
            if (!isComposite[(size_t)number]) {
                primes.push_back(number);
                if ((long long)number * number <= root) {
                    for (long long multiple = (long long)number * number;
                         multiple <= root;
                         multiple += number) {
                        isComposite[(size_t)multiple] = 1;
                    }
                }
            }
        }
    }

    void buildQuotients() {
        idSmall.assign((size_t)root + 1, -1);
        idLarge.assign((size_t)root + 1, -1);
        for (long long left = 1, right; left <= limit; left = right + 1) {
            long long value = limit / left;
            quotients.push_back(value);
            right = limit / value;
        }

        for (int index = 0; index < (int)quotients.size(); ++index) {
            long long value = quotients[(size_t)index];
            if (value <= root) {
                idSmall[(size_t)value] = index;
            } else {
                idLarge[(size_t)(limit / value)] = index;
            }
        }
    }

    void buildPowerSumInterpolation() {
        int degree = exponent + 1;
        powerSumPrefix.assign((size_t)degree + 1, 0);
        long long running = 0;
        for (int point = 1; point <= degree; ++point) {
            running += modularPower(point, exponent);
            running %= MODULUS;
            powerSumPrefix[(size_t)point] = (int)running;
        }

        std::vector<long long> factorials((size_t)degree + 1, 1);
        inverseFactorials.assign((size_t)degree + 1, 1);
        for (int i = 1; i <= degree; ++i) {
            factorials[(size_t)i] = factorials[(size_t)i - 1] * i % MODULUS;
        }
        inverseFactorials[(size_t)degree] =
            (int)modularPower(factorials[(size_t)degree], MODULUS - 2);
        for (int i = degree; i >= 1; --i) {
            inverseFactorials[(size_t)i - 1] =
                (long long)inverseFactorials[(size_t)i] * i % MODULUS;
        }
    }

    int powerSum(long long value) const {
        if (value <= 0) {
            return 0;
        }

        int degree = exponent + 1;
        if (value <= degree) {
            return powerSumPrefix[(size_t)value];
        }

        long long x = value % MODULUS;
        long long prefixProducts[64];
        long long suffixProducts[65];
        prefixProducts[0] = 1;
        for (int i = 0; i <= degree; ++i) {
            prefixProducts[i + 1] =
                prefixProducts[i] * normalize(x - i) % MODULUS;
        }
        suffixProducts[degree + 1] = 1;
        for (int i = degree; i >= 0; --i) {
            suffixProducts[i] =
                suffixProducts[i + 1] * normalize(x - i) % MODULUS;
        }

        long long result = 0;
        for (int i = 0; i <= degree; ++i) {
            long long numerator =
                prefixProducts[i] * suffixProducts[i + 1] % MODULUS;
            long long denominator =
                (long long)inverseFactorials[(size_t)i]
                * inverseFactorials[(size_t)(degree - i)]
                % MODULUS;
            if ((degree - i) & 1) {
                denominator = MODULUS - denominator;
            }
            result +=
                (long long)powerSumPrefix[(size_t)i]
                * numerator
                % MODULUS
                * denominator
                % MODULUS;
            result %= MODULUS;
        }
        return (int)result;
    }

    int quotientIndex(long long value) const {
        if (value <= root) {
            return idSmall[(size_t)value];
        }
        return idLarge[(size_t)(limit / value)];
    }

    void buildPrimePowerSums() {
        primePowers.assign(primes.size(), 0);
        primePowerPrefix.assign(primes.size() + 1, 0);
        for (int index = 0; index < (int)primes.size(); ++index) {
            primePowers[(size_t)index] =
                (int)modularPower(primes[(size_t)index], exponent);
            primePowerPrefix[(size_t)index + 1] =
                (
                    primePowerPrefix[(size_t)index]
                    + primePowers[(size_t)index]
                ) % MODULUS;
        }

        primePowerSums.resize(quotients.size());
        for (int index = 0; index < (int)quotients.size(); ++index) {
            primePowerSums[(size_t)index] =
                normalize(powerSum(quotients[(size_t)index]) - 1);
        }

        for (int primeIndex = 0;
             primeIndex < (int)primes.size();
             ++primeIndex) {
            long long prime = primes[(size_t)primeIndex];
            long long primeSquared = prime * prime;
            if (primeSquared > limit) {
                break;
            }

            long long primePower = primePowers[(size_t)primeIndex];
            for (int valueIndex = 0;
                 valueIndex < (int)quotients.size()
                 && quotients[(size_t)valueIndex] >= primeSquared;
                 ++valueIndex) {
                long long value = quotients[(size_t)valueIndex];
                int tail =
                    normalize(
                        primePowerSums[(size_t)quotientIndex(value / prime)]
                        - primePowerPrefix[(size_t)primeIndex]
                    );
                primePowerSums[(size_t)valueIndex] =
                    normalize(
                        primePowerSums[(size_t)valueIndex]
                        - primePower * tail
                    );
            }
        }
    }

    int primePowerSum(long long value) const {
        if (value < 2) {
            return 0;
        }
        return primePowerSums[(size_t)quotientIndex(value)];
    }

    int sumFromPrimeIndex(long long maxValue, int startPrimeIndex) const {
        if (maxValue < 2) {
            return 1;
        }
        if (
            startPrimeIndex < (int)primes.size()
            && maxValue < primes[(size_t)startPrimeIndex]
        ) {
            return 1;
        }

        long long result =
            1
            + primePowerSum(maxValue)
            - primePowerPrefix[(size_t)startPrimeIndex];
        result = normalize(result);

        for (int primeIndex = startPrimeIndex;
             primeIndex < (int)primes.size();
             ++primeIndex) {
            long long prime = primes[(size_t)primeIndex];
            if (prime * prime > maxValue) {
                break;
            }

            long long primePower = primePowers[(size_t)primeIndex];
            result +=
                primePower
                * normalize(
                    sumFromPrimeIndex(maxValue / prime, primeIndex + 1) - 1
                )
                % MODULUS;
            result %= MODULUS;

            long long primePowerValue = prime * prime;
            while (primePowerValue <= maxValue) {
                result +=
                    primePower
                    * sumFromPrimeIndex(
                        maxValue / primePowerValue,
                        primeIndex + 1
                    )
                    % MODULUS;
                result %= MODULUS;

                if (primePowerValue > maxValue / prime) {
                    break;
                }
                primePowerValue *= prime;
            }
        }

        return normalize(result);
    }
};

static int summedRadicalPowers(int maxExponent, long long limit) {
    SummatoryRadicalPowers solver(limit);
    long long result = 0;
    for (int exponent = 1; exponent <= maxExponent; ++exponent) {
        result += solver.solveExponent(exponent);
        result %= MODULUS;
    }
    return (int)result;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        return 1;
    }

    int maxExponent = std::atoi(argv[1]);
    long long limit = std::atoll(argv[2]);
    std::cout << summedRadicalPowers(maxExponent, limit) << "\n";
    return 0;
}
"""


def helperBinaryPath():
    digest = hashlib.sha256(CXX_SOURCE.encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "project_euler_639_" + digest)


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


def radical(number):
    result = 1
    factor = 2
    while factor * factor <= number:
        if number % factor == 0:
            result *= factor
            while number % factor == 0:
                number //= factor
        factor += 1 if factor == 2 else 2
    if number > 1:
        result *= number
    return result


def multiplicativeValue(number, exponent):
    return radical(number) ** exponent


def multiplicativeFunctionSum(exponent, limit):
    return sum(
        multiplicativeValue(number, exponent)
        for number in range(1, limit + 1)
    )


def multipleExponentSum(maxExponent, limit):
    binaryPath = compileHelper()
    output = subprocess.check_output(
        [binaryPath, str(maxExponent), str(limit)],
        text=True,
    )
    return int(output.strip())


def runTests():
    assert multiplicativeValue(2, 1) == 2
    assert multiplicativeValue(4, 1) == 2
    assert multiplicativeValue(18, 1) == 6
    assert multiplicativeValue(18, 2) == 36
    assert multiplicativeFunctionSum(1, 10) == 41
    assert multiplicativeFunctionSum(1, 100) == 3_512
    assert multiplicativeFunctionSum(2, 100) == 208_090
    assert multiplicativeFunctionSum(1, 10_000) == 35_252_550
    assert multipleExponentSum(1, 10) == 41
    assert multipleExponentSum(1, 100) == 3_512
    assert multipleExponentSum(1, 10_000) == 35_252_550
    assert multipleExponentSum(3, 10 ** 8) == 338_787_512


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = multipleExponentSum(50, 10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
