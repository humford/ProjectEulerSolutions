import collections
import time


LIMIT = 10**16


def countForRootsAndLength(roots, length):
    def possibleDigits(position):
        if length == 1:
            return range(1, 10)
        if position == 0 or position == length - 1:
            return range(1, 10)
        return range(10)

    start = (0,) * len(roots)
    counts = {start: 1}

    for position in range(length):
        next_counts = collections.defaultdict(int)

        for state, ways in counts.items():
            for digit in possibleDigits(position):
                next_state = []

                for carry, root in zip(state, roots):
                    total = carry + digit
                    if total % root != 0:
                        break
                    next_state.append(-(total // root))
                else:
                    next_counts[tuple(next_state)] += ways

        counts = next_counts
        if not counts:
            return 0

    return counts.get(start, 0)


def countWithIntegerRoot(limit):
    root_zero_count = limit // 10
    max_length = len(str(limit - 1))
    negative_root_count = 0

    for mask in range(1, 1 << 9):
        roots = tuple(root for root in range(1, 10) if (mask >> (root - 1)) & 1)
        sign = 1 if len(roots) & 1 else -1
        total = 0

        for length in range(1, max_length + 1):
            total += countForRootsAndLength(roots, length)

        negative_root_count += sign * total

    return root_zero_count + negative_root_count


def hasIntegerRoot(number):
    digits = [int(digit) for digit in str(number)]
    last_digit = digits[-1]

    if last_digit == 0:
        return True

    for divisor in range(1, last_digit + 1):
        if last_digit % divisor != 0:
            continue

        value = 0
        for digit in digits:
            value = value * (-divisor) + digit
        if value == 0:
            return True

    return False


def bruteCountWithIntegerRoot(limit):
    return sum(1 for number in range(1, limit + 1) if hasIntegerRoot(number))


def runTests():
    assert bruteCountWithIntegerRoot(100000) == 14696


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = countWithIntegerRoot(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
