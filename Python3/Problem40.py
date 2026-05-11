def champernowneDigit(position):
    digits = 1
    count = 9
    start = 1

    while position > digits * count:
        position -= digits * count
        digits += 1
        count *= 10
        start *= 10

    number = start + (position - 1) // digits
    digit_index = (position - 1) % digits
    return int(str(number)[digit_index])


def champernowneExpression():
    product = 1
    for position in (1, 10, 100, 1000, 10000, 100000, 1000000):
        product *= champernowneDigit(position)
    return product


def runTests():
    assert champernowneDigit(1) == 1
    assert champernowneDigit(12) == 1


def solve():
    return champernowneExpression()


if __name__ == "__main__":
    runTests()
    print(solve())
