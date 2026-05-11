def recurringCycleLength(denominator):
    seen = {}
    value = 1
    position = 0

    while value and value not in seen:
        seen[value] = position
        value = (value * 10) % denominator
        position += 1

    if value == 0:
        return 0
    return position - seen[value]


def denominatorWithLongestCycle(limit):
    best_denominator = 0
    best_length = 0

    for denominator in range(2, limit):
        length = recurringCycleLength(denominator)
        if length > best_length:
            best_denominator = denominator
            best_length = length

    return best_denominator


def runTests():
    assert recurringCycleLength(2) == 0
    assert recurringCycleLength(7) == 6
    assert denominatorWithLongestCycle(10) == 7


def solve():
    return denominatorWithLongestCycle(1000)


if __name__ == "__main__":
    runTests()
    print(solve())
