import time


MODULUS = 1_000_000_007


def smallestDigitSumNumber(digit_sum, modulus=None):
    nines, remainder = divmod(digit_sum, 9)
    if remainder == 0:
        value = 10 ** nines - 1 if modulus is None else (pow(10, nines, modulus) - 1) % modulus
    else:
        value = (remainder + 1) * (10 ** nines) - 1 if modulus is None else ((remainder + 1) * pow(10, nines, modulus) - 1) % modulus
    return value


def inverseDigitSumPrefix(limit, modulus=None):
    if modulus is None:
        return sum(smallestDigitSumNumber(n) for n in range(1, limit + 1))

    full_blocks, remainder = divmod(limit, 9)
    total = 0
    if full_blocks:
        total += 54 * (pow(10, full_blocks, modulus) - 1) * pow(9, modulus - 2, modulus)
        total -= 9 * full_blocks
    power = pow(10, full_blocks, modulus)
    for digit_sum_remainder in range(1, remainder + 1):
        total += (digit_sum_remainder + 1) * power - 1
    return total % modulus


def fibonacciNumbers(count):
    values = [0, 1]
    while len(values) <= count:
        values.append(values[-1] + values[-2])
    return values


def fibonacciInverseDigitSumTotal():
    fibs = fibonacciNumbers(90)
    return sum(inverseDigitSumPrefix(fibs[index], MODULUS) for index in range(2, 91)) % MODULUS


def runTests():
    assert smallestDigitSumNumber(10) == 19
    assert inverseDigitSumPrefix(20) == 1_074


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = fibonacciInverseDigitSumTotal()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
