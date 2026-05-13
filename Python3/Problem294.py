import math
import time


N = 11**12
DIVISOR = 23
DIGIT_SUM = 23
PERIOD = 22
MODULUS = 10**9


def boundedDigitSumCount(places, digit_sum):
    if places == 0:
        return 1 if digit_sum == 0 else 0

    total = 0

    for overfilled in range(digit_sum // 10 + 1):
        if overfilled <= places:
            total += (
                (-1 if overfilled % 2 else 1)
                * math.comb(places, overfilled)
                * math.comb(digit_sum - 10 * overfilled + places - 1, places - 1)
            )

    return total


def digitSumDivisibilityCount(length):
    full_periods, extra_places = divmod(length, PERIOD)
    states = {(0, 0): 1}

    for position in range(PERIOD):
        place_count = full_periods + (1 if position < extra_places else 0)
        residue_weight = pow(10, position, DIVISOR)
        counts = [
            boundedDigitSumCount(place_count, digit_sum) % MODULUS
            for digit_sum in range(DIGIT_SUM + 1)
        ]
        next_states = {}

        for (current_sum, residue), value in states.items():
            for added_sum, count in enumerate(counts[: DIGIT_SUM + 1 - current_sum]):
                if count == 0:
                    continue

                key = (
                    current_sum + added_sum,
                    (residue + residue_weight * added_sum) % DIVISOR,
                )
                next_states[key] = (next_states.get(key, 0) + value * count) % MODULUS

        states = next_states

    return states.get((DIGIT_SUM, 0), 0)


def runTests():
    assert digitSumDivisibilityCount(9) == 263626
    assert digitSumDivisibilityCount(42) == 6377168878570056 % MODULUS


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = digitSumDivisibilityCount(N)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
