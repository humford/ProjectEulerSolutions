import array
import time


LIMIT = 150


FACTORIALS = [1] * 10
for digit in range(2, 10):
    FACTORIALS[digit] = FACTORIALS[digit - 1] * digit

NINE_FACTORIAL = FACTORIALS[9]


def digitSum(number):
    result = 0

    while number:
        number, digit = divmod(number, 10)
        result += digit

    return result


def factorialDigitSum(number):
    result = 0

    while number:
        number, digit = divmod(number, 10)
        result += FACTORIALS[digit]

    return result


def summedFactorialDigitSum(number):
    return digitSum(factorialDigitSum(number))


def smallestNumberWithDigitSum(total):
    nines, leading = divmod(total, 9)
    if leading == 0:
        return int("9" * nines)
    return int(str(leading) + "9" * nines)


def precomputedDigitSums(limit):
    sums = array.array("B", [0]) * (limit + 1)

    for number in range(1, limit + 1):
        sums[number] = sums[number // 10] + number % 10

    return sums


def buildRemainderData():
    digit_counts = [bytearray(NINE_FACTORIAL) for _ in range(9)]
    remainder_lengths = bytearray(NINE_FACTORIAL)
    remainder_digit_sums = array.array("H", [0]) * NINE_FACTORIAL
    packed_buckets = [[] for _ in range(9)]

    for remainder in range(NINE_FACTORIAL):
        remaining = remainder
        counts = [0] * 9

        for digit in range(8, 0, -1):
            counts[digit], remaining = divmod(remaining, FACTORIALS[digit])

        length = sum(counts)
        digit_sum = sum(digit * counts[digit] for digit in range(1, 9))

        remainder_lengths[remainder] = length
        remainder_digit_sums[remainder] = digit_sum

        code = length
        for digit in range(1, 9):
            digit_counts[digit][remainder] = counts[digit]
            code = code * 9 + (8 - counts[digit])

        packed_buckets[remainder % 9].append((code << 19) | remainder)

    mask = (1 << 19) - 1
    buckets = []
    for packed in packed_buckets:
        packed.sort()
        buckets.append([value & mask for value in packed])

    return buckets, digit_counts, remainder_lengths, remainder_digit_sums


def sumOfSg(limit):
    low_digit_sums = precomputedDigitSums(1000000 + NINE_FACTORIAL - 1)
    buckets, digit_counts, remainder_lengths, remainder_digit_sums = buildRemainderData()
    result = 0

    for target in range(1, limit + 1):
        minimum_sum_value = smallestNumberWithDigitSum(target)
        minimum_nines = minimum_sum_value // NINE_FACTORIAL
        best_key = None
        best_digit_sum = None

        for extra_nines in range(37):
            nines = minimum_nines + extra_nines
            if best_key is not None and nines >= best_key[0]:
                break

            base = nines * NINE_FACTORIAL
            high, low = divmod(base, 1000000)
            high_sum = digitSum(high)
            high_carry_sum = digitSum(high + 1)
            needed_low_sum = target - high_sum
            needed_low_carry_sum = target - high_carry_sum

            if needed_low_sum < 0 or needed_low_sum > 54:
                needed_low_sum = -1
            if needed_low_carry_sum < 0 or needed_low_carry_sum > 54:
                needed_low_carry_sum = -1

            found_remainder = None
            for remainder in buckets[target % 9]:
                low_part = low + remainder
                if low_part < 1000000:
                    if (
                        needed_low_sum >= 0
                        and low_digit_sums[low_part] == needed_low_sum
                    ):
                        found_remainder = remainder
                        break
                elif (
                    needed_low_carry_sum >= 0
                    and low_digit_sums[low_part - 1000000] == needed_low_carry_sum
                ):
                    found_remainder = remainder
                    break

            if found_remainder is None:
                continue

            remainder = found_remainder
            key = (
                nines + remainder_lengths[remainder],
                -digit_counts[1][remainder],
                -digit_counts[2][remainder],
                -digit_counts[3][remainder],
                -digit_counts[4][remainder],
                -digit_counts[5][remainder],
                -digit_counts[6][remainder],
                -digit_counts[7][remainder],
                -digit_counts[8][remainder],
                -nines,
            )

            if best_key is None or key < best_key:
                best_key = key
                best_digit_sum = remainder_digit_sums[remainder] + 9 * nines

        assert best_digit_sum is not None
        result += best_digit_sum

    return result


def bruteG(target, limit):
    for number in range(1, limit + 1):
        if summedFactorialDigitSum(number) == target:
            return number
    raise AssertionError("brute force limit exceeded")


def runTests():
    assert factorialDigitSum(342) == 32
    assert summedFactorialDigitSum(342) == 5
    assert summedFactorialDigitSum(25) == 5
    assert bruteG(5, 1000) == 25
    assert bruteG(20, 1000) == 267
    assert sumOfSg(20) == 156


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumOfSg(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
