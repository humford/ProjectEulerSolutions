import time


LIMIT = 10**18
MODULUS = 10**8


def fibonacciNumbers(limit):
    fibs = [0, 1, 2]

    while fibs[-1] <= limit:
        fibs.append(fibs[-1] + fibs[-2])

    return fibs


def maximumFirstMove(number, fibs):
    if number <= 1:
        return 0

    index = len(fibs) - 1

    while fibs[index] > number:
        index -= 1

    if fibs[index] == number:
        return 0

    remaining = number - fibs[index]

    while index >= 3 and 2 * remaining >= fibs[index]:
        remaining -= fibs[index - 2]
        index -= 2

    return remaining


def maximumFirstMoveSum(limit=LIMIT, modulus=MODULUS):
    fibs = fibonacciNumbers(limit + 1)
    total = 0

    for index in range(1, len(fibs) - 1):
        current = fibs[index]

        if current > limit:
            break

        maximumRemainder = min(fibs[index + 1] - 1, limit) - current

        if index - 1 < 1:
            continue

        maximumRemainder = min(maximumRemainder, fibs[index - 1] - 1)

        if maximumRemainder <= 0:
            continue

        subtracted = 0
        lower = 1
        stage = 0

        while True:
            stageIndex = index - 2 * stage

            if stageIndex < 1:
                break

            upper = min(maximumRemainder, subtracted + (fibs[stageIndex] - 1) // 2)

            if lower <= upper:
                count = upper - lower + 1
                total = (
                    total
                    + (lower + upper) * count // 2
                    - count * subtracted
                ) % modulus

            if stageIndex - 2 < 1:
                break

            lower = max(lower, subtracted + (fibs[stageIndex] + 1) // 2)
            subtracted += fibs[stageIndex - 2]
            stage += 1

            if lower > maximumRemainder:
                break

    return total % modulus


def runTests():
    fibs = fibonacciNumbers(1000)
    assert maximumFirstMove(5, fibs) == 0
    assert maximumFirstMove(17, fibs) == 4
    assert maximumFirstMoveSum(100) == 728


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumFirstMoveSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
