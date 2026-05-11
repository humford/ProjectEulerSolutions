import numpy as np


def factorialPrimeValuations(limit, prime):
    values = np.zeros(limit + 1, dtype=np.int32)

    for n in range(1, limit + 1):
        value = n
        exponent = 0
        while value % prime == 0:
            exponent += 1
            value //= prime
        values[n] = values[n - 1] + exponent

    return values


def divisibleCoefficientCount(size, divisor_power):
    twos = factorialPrimeValuations(size, 2)
    fives = factorialPrimeValuations(size, 5)
    max_two_sum = int(twos[size] - divisor_power)
    max_five_sum = int(fives[size] - divisor_power)
    count = 0

    for a in range(size // 3 + 1):
        b_start = a
        b_end = (size - a) // 2
        max_pair_twos = max_two_sum - int(twos[a])
        max_pair_fives = max_five_sum - int(fives[a])

        fives_b = fives[b_start : b_end + 1]
        fives_c = fives[size - a - b_end : size - a - b_start + 1][::-1]
        valid = fives_b + fives_c <= max_pair_fives

        if not valid.any():
            continue

        twos_b = twos[b_start : b_end + 1]
        twos_c = twos[size - a - b_end : size - a - b_start + 1][::-1]
        valid &= twos_b + twos_c <= max_pair_twos
        valid_count = int(np.count_nonzero(valid))
        if valid_count == 0:
            continue

        count += 6 * valid_count
        if valid[0]:
            count -= 3

        if (size - a) % 2 == 0:
            equal_bc_index = (size - a) // 2 - b_start
            if 0 <= equal_bc_index < len(valid) and valid[equal_bc_index]:
                count -= 3

        if size % 3 == 0 and a == size // 3 and valid[0]:
            count += 1

    return count


def bruteDivisibleCoefficientCount(size, divisor_power):
    twos = factorialPrimeValuations(size, 2)
    fives = factorialPrimeValuations(size, 5)
    count = 0

    for a in range(size + 1):
        for b in range(size - a + 1):
            c = size - a - b
            two_count = twos[size] - twos[a] - twos[b] - twos[c]
            five_count = fives[size] - fives[a] - fives[b] - fives[c]
            if two_count >= divisor_power and five_count >= divisor_power:
                count += 1

    return count


def runTests():
    assert divisibleCoefficientCount(20, 2) == bruteDivisibleCoefficientCount(20, 2)


def solve():
    return divisibleCoefficientCount(200000, 12)


if __name__ == "__main__":
    runTests()
    print(solve())
