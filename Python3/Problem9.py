from math import gcd


def pythagoreanTripletWithSum(total):
    for m in range(2, int(total ** 0.5) + 1):
        for n in range(1, m):
            if (m - n) % 2 == 0 or gcd(m, n) != 1:
                continue

            primitive_sum = 2 * m * (m + n)
            if total % primitive_sum != 0:
                continue

            scale = total // primitive_sum
            a = scale * (m * m - n * n)
            b = scale * (2 * m * n)
            c = scale * (m * m + n * n)
            return tuple(sorted((a, b, c)))

    raise ValueError("No Pythagorean triplet found for sum %s" % total)


def tripletProductForSum(total):
    a, b, c = pythagoreanTripletWithSum(total)
    return a * b * c


def runTests():
    assert pythagoreanTripletWithSum(12) == (3, 4, 5)
    assert tripletProductForSum(12) == 60


def solve():
    return tripletProductForSum(1000)


if __name__ == "__main__":
    runTests()
    print(solve())
