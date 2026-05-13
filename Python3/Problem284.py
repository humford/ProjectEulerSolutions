import time


LIMIT = 10000
BASE = 14
DIGITS = "0123456789abcd"


def toBase(number, base):
    if number == 0:
        return "0"

    result = []

    while number:
        number, digit = divmod(number, base)
        result.append(DIGITS[digit])

    return "".join(reversed(result))


def steadySquareDigitSum(limit):
    states = []

    for value in (0, 1, 7, 8):
        modulus = BASE
        quotient = (value * value - value) // modulus
        digit_sum = value
        states.append([value, modulus, quotient, digit_sum])

    total = 0

    for length in range(1, limit + 1):
        for value, modulus, quotient, digit_sum in states:
            if value != 0 and value >= modulus // BASE:
                total += digit_sum

        if length == limit:
            break

        for state in states:
            value, modulus, quotient, digit_sum = state
            next_digit = (
                -quotient * pow((2 * value - 1) % BASE, -1, BASE)
            ) % BASE

            state[0] = value + next_digit * modulus
            state[1] = modulus * BASE
            state[2] = (
                quotient
                + next_digit * (2 * value - 1)
                + next_digit * next_digit * modulus
            ) // BASE
            state[3] = digit_sum + next_digit

    return total


def runTests():
    assert toBase(582, BASE) == "2d8"
    assert toBase(steadySquareDigitSum(9), BASE) == "2d8"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = toBase(steadySquareDigitSum(LIMIT), BASE)
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
