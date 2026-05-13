import math
import time


def diagramRows(limit):
    rows = []
    power3 = 1
    while power3 <= limit:
        remaining = limit // power3
        power2 = 1
        exponent2 = 0
        while power2 * 2 <= remaining:
            power2 *= 2
            exponent2 += 1
        rows.append(exponent2 + 1)
        power3 *= 3
    return rows


def hookLengths(rows):
    columns = [0] * max(rows)
    for rowLength in rows:
        for column in range(rowLength):
            columns[column] += 1

    hooks = []
    for row, rowLength in enumerate(rows):
        for column in range(rowLength):
            right = rowLength - column - 1
            below = columns[column] - row - 1
            hooks.append(right + below + 1)
    return hooks


def permutationCount(limit):
    rows = diagramRows(limit)
    count = math.factorial(sum(rows))
    for hook in hookLengths(rows):
        count //= hook
    return count


def scientificNotation(value, places=10):
    digits = str(value)
    exponent = len(digits) - 1
    kept = places + 1
    mantissa = int(digits[:kept].ljust(kept, "0"))
    if len(digits) > kept and int(digits[kept]) >= 5:
        mantissa += 1
    if mantissa == 10 ** kept:
        mantissa //= 10
        exponent += 1

    mantissaText = str(mantissa).rjust(kept, "0")
    return mantissaText[0] + "." + mantissaText[1:] + "e" + str(exponent)


def runTests():
    assert permutationCount(6) == 5
    assert permutationCount(8) == 9
    assert permutationCount(20) == 450
    assert scientificNotation(permutationCount(1000)) == "8.8521816557e21"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = scientificNotation(permutationCount(10 ** 18))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
