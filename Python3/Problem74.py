import math
import time


DIGIT_FACTORIALS = [math.factorial(n) for n in range(10)]


def digitFactorialSum(n):
    return sum(DIGIT_FACTORIALS[int(digit)] for digit in str(n))


def chainLength(n, memo):
    sequence = []
    seen = {}
    current = n

    while current not in memo and current not in seen:
        seen[current] = len(sequence)
        sequence.append(current)
        current = digitFactorialSum(current)

    if current in memo:
        length = memo[current]
        for value in reversed(sequence):
            length += 1
            memo[value] = length
    else:
        cycle_start = seen[current]
        cycle_length = len(sequence) - cycle_start

        for value in sequence[cycle_start:]:
            memo[value] = cycle_length

        length = cycle_length
        for value in reversed(sequence[:cycle_start]):
            length += 1
            memo[value] = length

    return memo[n]


def chainsWithLength(limit, target_length):
    memo = {}
    return sum(chainLength(n, memo) == target_length for n in range(1, limit))


def runTests():
    memo = {}
    assert digitFactorialSum(145) == 145
    assert chainLength(69, memo) == 5
    assert chainLength(78, memo) == 4
    assert chainLength(540, memo) == 2
    assert chainLength(169, memo) == 3


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = chainsWithLength(1000000, 60)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
