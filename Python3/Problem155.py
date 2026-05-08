import math
import time


def normalize(numerator, denominator):
    divisor = math.gcd(numerator, denominator)
    return numerator // divisor, denominator // divisor


def distinctCapacitanceCount(limit):
    exact = [set() for _ in range(limit + 1)]
    exact[1].add((1, 1))
    all_values = {(1, 1)}

    for total in range(2, limit + 1):
        values = set()

        for left_count in range(1, total // 2 + 1):
            right_count = total - left_count
            for left_num, left_den in exact[left_count]:
                for right_num, right_den in exact[right_count]:
                    parallel_num = left_num * right_den + right_num * left_den
                    parallel_den = left_den * right_den
                    values.add(normalize(parallel_num, parallel_den))
                    values.add(normalize(left_num * right_num, parallel_num))

        exact[total] = values
        all_values.update(values)

    return len(all_values)


def runTests():
    assert distinctCapacitanceCount(3) == 7


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = distinctCapacitanceCount(18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
