def isPandigital(value):
    digits = str(value)
    return len(digits) == 9 and set(digits) == set("123456789")


def concatenatedProduct(integer, count):
    return int("".join(str(integer * multiplier) for multiplier in range(1, count + 1)))


def largestPandigitalMultiple():
    largest = 0
    for integer in range(1, 10000):
        combined = ""
        multiplier = 1
        while len(combined) < 9:
            combined += str(integer * multiplier)
            multiplier += 1
        if isPandigital(combined):
            largest = max(largest, int(combined))
    return largest


def runTests():
    assert concatenatedProduct(192, 3) == 192384576
    assert isPandigital(192384576)


def solve():
    return largestPandigitalMultiple()


if __name__ == "__main__":
    runTests()
    print(solve())
