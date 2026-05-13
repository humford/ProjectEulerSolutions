import time


MODULUS = 1_000_000_007


def baseDigits(n, base):
    if n == 0:
        return [0]

    digits = []
    while n:
        digits.append(n % base)
        n //= base
    return list(reversed(digits))


def _add(value, increment, modulus):
    value += increment
    if modulus is not None:
        value %= modulus
    return value


def transformCoefficients(base, maxOrder, modulus=None):
    coefficients = []
    zero = [0] * (maxOrder + 2)

    coefficients.append([])
    for _ in range(base):
        row = zero[:]
        row[1] = 1
        coefficients[0].append(row)

    for order in range(1, maxOrder + 1):
        coefficients.append([])
        fullBlock = zero[:]

        for digit in range(base):
            for index, value in enumerate(coefficients[order - 1][digit]):
                fullBlock[index] = _add(fullBlock[index], value, modulus)

        partialBlock = zero[:]
        for digit in range(base):
            for index, value in enumerate(coefficients[order - 1][digit]):
                partialBlock[index] = _add(partialBlock[index], value, modulus)

            row = zero[:]
            for index, value in enumerate(fullBlock):
                if value:
                    row[index] = _add(row[index], -value, modulus)
                    row[index + 1] = _add(row[index + 1], value, modulus)
            for index, value in enumerate(partialBlock):
                if value:
                    row[index] = _add(row[index], value, modulus)

            coefficients[order].append(row)

    return coefficients


def floorRecursion(k, n, modulus=None):
    digits = baseDigits(n, k)
    maxOrder = len(digits) + 1
    coefficients = transformCoefficients(k, maxOrder, modulus)
    values = [1] * (maxOrder + 2)
    activeOrders = maxOrder + 1

    for digit in digits:
        previous = values[:]
        for order in range(activeOrders):
            total = 0
            for index, coefficient in enumerate(coefficients[order][digit]):
                if coefficient:
                    total += coefficient * previous[index]
            if modulus is not None:
                total %= modulus
            values[order] = total
        activeOrders -= 1

    return values[1]


def floorRecursionSum(n, modulus=MODULUS):
    return sum(floorRecursion(k, n, modulus) for k in range(2, 11)) % modulus


def runTests():
    assert floorRecursion(5, 10) == 18
    assert floorRecursion(7, 100) == 1_003
    assert floorRecursion(2, 10 ** 3) == 264_830_889_564


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = floorRecursionSum(10 ** 14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
