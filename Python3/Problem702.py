import time


def inversionCountModMultiplication(multiplier, modulus, memo):
    if modulus <= 2:
        return 0

    multiplier %= modulus
    if multiplier in (0, 1):
        return 0
    if multiplier == modulus - 1:
        return (modulus - 1) * (modulus - 2) // 2

    key = (multiplier, modulus)
    if key in memo:
        return memo[key]

    quotient = modulus // multiplier
    remainder = modulus - quotient * multiplier
    block = (quotient * (quotient + 1) // 2) * (multiplier * (multiplier - 1) // 2)
    result = (
        block
        + (quotient + 1) * inversionCountModMultiplication(multiplier, remainder, memo)
        - quotient * inversionCountModMultiplication(multiplier, multiplier - remainder, memo)
    )

    memo[key] = result
    return result


def orientationCount(multiplier, modulus, memo):
    if modulus <= 2:
        return 0
    return (modulus - 1) * (modulus - 2) - inversionCountModMultiplication(multiplier, modulus, memo)


def jumpingFleaSum(sideLength):
    if sideLength <= 0:
        raise ValueError("side length must be positive")
    if sideLength % 2 == 0:
        raise ValueError("this reduction requires an odd side length")

    memo = {}
    depth = sideLength.bit_length()
    total = (sideLength * (3 * sideLength + 1) // 2) * (depth + 1)

    for d in range(2, depth + 1):
        total -= orientationCount(sideLength, 1 << d, memo)

    total += 2 * orientationCount(sideLength, (1 << depth) - sideLength, memo)
    return total


def runTests():
    assert jumpingFleaSum(3) == 42
    assert jumpingFleaSum(5) == 126
    assert jumpingFleaSum(123) == 167_178
    assert jumpingFleaSum(12_345) == 3_185_041_956


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = jumpingFleaSum(123_456_789)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
