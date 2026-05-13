import time


LIMIT = 10**15
TARGET_STEPS = "UDDDUdddDDUDDddDdDddDDUDDdUUDd"


def firstValueWithStepPrefix(steps, minimum):
    multiplier = 1
    offset = 0
    denominator = 1

    for step in steps:
        if step == "U":
            multiplier *= 4
            offset = 4 * offset + 2 * denominator
        elif step == "d":
            multiplier *= 2
            offset = 2 * offset - denominator
        elif step != "D":
            raise ValueError("unknown step")

        denominator *= 3

    residue = (-offset * pow(multiplier, -1, denominator)) % denominator

    if residue > minimum:
        return residue

    return residue + ((minimum - residue) // denominator + 1) * denominator


def stepPrefix(value, length):
    result = []

    for _ in range(length):
        remainder = value % 3

        if remainder == 0:
            result.append("D")
            value //= 3
        elif remainder == 1:
            result.append("U")
            value = (4 * value + 2) // 3
        else:
            result.append("d")
            value = (2 * value - 1) // 3

    return "".join(result)


def runTests():
    sample = "DdDddUUdDD"
    assert firstValueWithStepPrefix(sample, 10**6) == 1004064
    assert stepPrefix(231, 10) == sample


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = firstValueWithStepPrefix(TARGET_STEPS, LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
