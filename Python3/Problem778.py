import time


MOD = 1_000_000_009


def freshmanProduct(a, b):
    result = 0
    place = 1
    while a or b:
        result += ((a % 10) * (b % 10) % 10) * place
        place *= 10
        a //= 10
        b //= 10
    return result


def digitCountsUpTo(limit, position):
    base = 10 ** position
    higher = limit // (10 * base)
    current = (limit // base) % 10
    lower = limit % base

    counts = [higher * base] * 10
    for digit in range(current):
        counts[digit] += base
    counts[current] += lower + 1
    return counts


def matrixMultiply(left, right, modulus=MOD):
    result = [[0] * 10 for _ in range(10)]
    for i in range(10):
        for k in range(10):
            value = left[i][k]
            if not value:
                continue
            for j in range(10):
                result[i][j] = (result[i][j] + value * right[k][j]) % modulus
    return result


def matrixPower(matrix, exponent, modulus=MOD):
    result = [[0] * 10 for _ in range(10)]
    for i in range(10):
        result[i][i] = 1

    while exponent:
        if exponent & 1:
            result = matrixMultiply(result, matrix, modulus)
        matrix = matrixMultiply(matrix, matrix, modulus)
        exponent //= 2
    return result


def F(repetitions, limit, modulus=MOD):
    answer = 0
    place = 1
    for position in range(len(str(limit))):
        counts = digitCountsUpTo(limit, position)
        transition = [[0] * 10 for _ in range(10)]
        for state in range(10):
            for digit in range(10):
                transition[state][state * digit % 10] += counts[digit]
        powered = matrixPower(transition, repetitions, modulus)
        digitSum = sum(digit * ways for digit, ways in enumerate(powered[1])) % modulus
        answer = (answer + digitSum * place) % modulus
        place = place * 10 % modulus
    return answer


def bruteF(repetitions, limit):
    total = 0

    def extend(depth, current):
        nonlocal total
        if depth == repetitions:
            total += current
            return
        for value in range(limit + 1):
            extend(depth + 1, freshmanProduct(current, value))

    for first in range(limit + 1):
        extend(1, first)
    return total


def runTests():
    assert freshmanProduct(234, 765) == 480
    assert F(2, 7) == 204
    assert F(3, 9) == bruteF(3, 9)
    assert F(23, 76) == 5_870_548


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = F(234_567, 765_432)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
