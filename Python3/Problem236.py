import math
import time


A = [5248, 1312, 2624, 5760, 3936]
B = [640, 1888, 3776, 3776, 5664]
TOTAL_A = sum(A)
TOTAL_B = sum(B)


def candidateRatios():
    candidates = set()
    a = A[0]
    b = B[0]

    for spoiled_a in range(1, a + 1):
        first_spoiled_b = spoiled_a * b // a + 1
        for spoiled_b in range(first_spoiled_b, b + 1):
            numerator = spoiled_b * a
            denominator = spoiled_a * b
            divisor = math.gcd(numerator, denominator)
            candidates.add((numerator // divisor, denominator // divisor))

    return candidates


def isPossible(numerator, denominator):
    coefficients = []
    ranges = []

    for supplied_a, supplied_b in zip(A, B):
        pair_numerator = supplied_b * numerator
        pair_denominator = supplied_a * denominator
        divisor = math.gcd(pair_numerator, pair_denominator)
        bad_b_step = pair_numerator // divisor
        bad_a_step = pair_denominator // divisor
        maximum = min(supplied_a // bad_a_step, supplied_b // bad_b_step)

        if maximum < 1:
            return False

        coefficients.append(
            denominator * bad_a_step * TOTAL_B
            - numerator * bad_b_step * TOTAL_A
        )
        ranges.append(maximum)

    left_sums = set()
    for t0 in range(1, ranges[0] + 1):
        first = coefficients[0] * t0
        for t1 in range(1, ranges[1] + 1):
            left_sums.add(first + coefficients[1] * t1)

    for t2 in range(1, ranges[2] + 1):
        third = coefficients[2] * t2
        for t3 in range(1, ranges[3] + 1):
            partial = third + coefficients[3] * t3
            for t4 in range(1, ranges[4] + 1):
                if -(partial + coefficients[4] * t4) in left_sums:
                    return True

    return False


def feasibleRatios():
    return [
        ratio
        for ratio in candidateRatios()
        if isPossible(ratio[0], ratio[1])
    ]


def largestRatio():
    ratios = feasibleRatios()
    return max(ratios, key=lambda ratio: ratio[0] / ratio[1])


def runTests(ratios):
    assert len(ratios) == 35
    assert min(ratios, key=lambda ratio: ratio[0] / ratio[1]) == (1476, 1475)


if __name__ == "__main__":
    start = time.time()
    ratios = feasibleRatios()
    runTests(ratios)
    numerator, denominator = max(ratios, key=lambda ratio: ratio[0] / ratio[1])
    elapsed = time.time() - start

    print(
        "Found "
        + str(numerator)
        + "/"
        + str(denominator)
        + " in "
        + str(elapsed)
        + " seconds."
    )
