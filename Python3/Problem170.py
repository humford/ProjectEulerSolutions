import itertools
import math
import time


DIGITS = set("0123456789")


def splitPositions():
    return [
        [index + 1 for index in range(9) if mask & (1 << index)]
        for mask in range(1, 1 << 9)
    ]


def divisors(n):
    values = []
    factor = 1

    while factor * factor <= n:
        if n % factor == 0:
            values.append(factor)
            if factor * factor != n:
                values.append(n // factor)
        factor += 1

    return values


def isPandigital(text):
    return len(text) == 10 and set(text) == DIGITS


def validInputForProduct(product_text):
    for positions in splitPositions():
        chunks = []
        start = 0
        invalid = False

        for position in positions + [10]:
            if product_text[start] == "0":
                invalid = True
                break
            chunks.append(int(product_text[start:position]))
            start = position
        if invalid:
            continue

        common_divisor = 0
        for chunk in chunks:
            common_divisor = math.gcd(common_divisor, chunk)
        if common_divisor < 2:
            continue

        for multiplier in divisors(common_divisor):
            if multiplier < 2:
                continue
            input_text = str(multiplier) + "".join(str(chunk // multiplier) for chunk in chunks)
            if isPandigital(input_text):
                return True

    return False


def largestPandigitalConcatenatedProduct():
    for permutation in itertools.permutations("9876543210"):
        candidate = "".join(permutation)
        if candidate[0] != "0" and validInputForProduct(candidate):
            return candidate

    raise ValueError("No product found")


def runTests():
    assert isPandigital("6127398540")


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestPandigitalConcatenatedProduct()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
