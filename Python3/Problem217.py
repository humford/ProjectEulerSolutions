import time


MODULUS = 3 ** 15


def blockData(length, leading_zero_allowed, modulus):
    max_sum = 9 * length
    counts = [0] * (max_sum + 1)
    sums = [0] * (max_sum + 1)

    if length == 0:
        counts[0] = 1
        return counts, sums

    first_digits = range(10) if leading_zero_allowed else range(1, 10)
    for digit in first_digits:
        counts[digit] += 1
        sums[digit] += digit

    current_max = 9
    for _ in range(1, length):
        next_counts = [0] * (max_sum + 1)
        next_sums = [0] * (max_sum + 1)

        for digit_sum in range(current_max + 1):
            count = counts[digit_sum]
            value_sum = sums[digit_sum]
            if count == 0:
                continue

            for digit in range(10):
                next_sum = digit_sum + digit
                next_counts[next_sum] = (next_counts[next_sum] + count) % modulus
                next_sums[next_sum] = (
                    next_sums[next_sum] + value_sum * 10 + digit * count
                ) % modulus

        counts, sums = next_counts, next_sums
        current_max += 9

    return counts, sums


def balancedLengthSum(length, modulus):
    if length == 1:
        return 45 % modulus

    half = length // 2
    middle_digits = length % 2
    left_counts, left_sums = blockData(half, False, modulus)
    right_counts, right_sums = blockData(half, True, modulus)
    power_right = pow(10, half, modulus)
    power_middle = pow(10, half, modulus)
    total = 0

    for digit_sum in range(9 * half + 1):
        left_count = left_counts[digit_sum]
        right_count = right_counts[digit_sum]
        if left_count == 0 or right_count == 0:
            continue

        if middle_digits:
            total += (
                10 * left_sums[digit_sum] * pow(10, half + 1, modulus) * right_count
                + 45 * power_middle * left_count * right_count
                + 10 * left_count * right_sums[digit_sum]
            )
        else:
            total += (
                left_sums[digit_sum] * power_right * right_count
                + left_count * right_sums[digit_sum]
            )

    return total % modulus


def balancedTotal(limit, modulus=MODULUS):
    return sum(balancedLengthSum(length, modulus) for length in range(1, limit + 1)) % modulus


def runTests():
    assert balancedTotal(1) == 45
    assert balancedTotal(2) == 540


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = balancedTotal(47)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
