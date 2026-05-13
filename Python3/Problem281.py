import functools
import math
import time


LIMIT = 10**15


def divisors(number):
    result = []

    for divisor in range(1, math.isqrt(number) + 1):
        if number % divisor == 0:
            result.append(divisor)
            if divisor * divisor != number:
                result.append(number // divisor)

    return result


@functools.lru_cache(maxsize=None)
def totient(number):
    result = number
    factor = 2
    remaining = number

    while factor * factor <= remaining:
        if remaining % factor == 0:
            while remaining % factor == 0:
                remaining //= factor
            result -= result // factor

        factor += 1 if factor == 2 else 2

    if remaining > 1:
        result -= result // remaining

    return result


def pizzaToppingCount(topping_count, pieces_per_topping):
    slice_count = topping_count * pieces_per_topping
    total = 0

    for cycle_length in divisors(pieces_per_topping):
        reduced_count = pieces_per_topping // cycle_length
        fixed_rotations = math.factorial(slice_count // cycle_length) // (
            math.factorial(reduced_count) ** topping_count
        )
        total += totient(cycle_length) * fixed_rotations

    return total // slice_count


def pizzaToppingSum(limit):
    total = 0
    topping_count = 2

    while pizzaToppingCount(topping_count, 1) <= limit:
        pieces_per_topping = 1

        while True:
            count = pizzaToppingCount(topping_count, pieces_per_topping)
            if count > limit:
                break

            total += count
            pieces_per_topping += 1

        topping_count += 1

    return total


def runTests():
    assert pizzaToppingCount(2, 1) == 1
    assert pizzaToppingCount(2, 2) == 2
    assert pizzaToppingCount(3, 1) == 2
    assert pizzaToppingCount(3, 2) == 16


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pizzaToppingSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
