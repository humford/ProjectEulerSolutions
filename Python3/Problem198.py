import time


def nontrivialAmbiguousCount(denominator_limit, reciprocal_limit):
    max_product = denominator_limit // 2
    total = 0
    stack = [(0, 1, 1, 1)]

    while stack:
        left_numerator, left_denominator, right_numerator, right_denominator = stack.pop()

        if left_denominator * right_denominator > max_product:
            continue
        if reciprocal_limit * left_numerator >= left_denominator:
            continue

        if (
            left_numerator > 0
            and reciprocal_limit
            * (
                left_numerator * right_denominator
                + left_denominator * right_numerator
            )
            < 2 * left_denominator * right_denominator
        ):
            total += 1

        mediant_numerator = left_numerator + right_numerator
        mediant_denominator = left_denominator + right_denominator

        if left_denominator * mediant_denominator <= max_product:
            stack.append(
                (
                    left_numerator,
                    left_denominator,
                    mediant_numerator,
                    mediant_denominator,
                )
            )

        if (
            right_denominator * mediant_denominator <= max_product
            and reciprocal_limit * mediant_numerator < mediant_denominator
        ):
            stack.append(
                (
                    mediant_numerator,
                    mediant_denominator,
                    right_numerator,
                    right_denominator,
                )
            )

    return total


def ambiguousCount(denominator_limit, reciprocal_limit):
    trivial = max(0, denominator_limit // 2 - reciprocal_limit // 2)
    return trivial + nontrivialAmbiguousCount(denominator_limit, reciprocal_limit)


def runTests():
    assert ambiguousCount(100000, 100) == 50271
    assert ambiguousCount(1000000, 100) == 509763


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = ambiguousCount(10 ** 8, 100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
