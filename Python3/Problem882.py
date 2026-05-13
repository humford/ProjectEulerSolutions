from fractions import Fraction
import time


TARGET_N = 10**5


def removeBitMoves(number, bit):
    bits = bin(number)[2:]
    moves = set()

    for index, currentBit in enumerate(bits):
        if currentBit != bit:
            continue

        remaining = bits[:index] + bits[index + 1:]
        moves.add(int(remaining, 2) if remaining else 0)

    return moves


def simplestDyadicBetween(leftBound, rightBound):
    if rightBound is None:
        return Fraction(leftBound.numerator // leftBound.denominator + 1, 1)

    exponent = 0
    while True:
        denominator = 1 << exponent
        scaledLeft = leftBound * denominator
        scaledRight = rightBound * denominator

        numeratorMin = scaledLeft.numerator // scaledLeft.denominator + 1
        numeratorMax = (scaledRight.numerator - 1) // scaledRight.denominator
        if numeratorMin <= numeratorMax:
            return Fraction(numeratorMin, denominator)

        exponent += 1


def gameValues(limit):
    values = [Fraction(0)]

    for number in range(1, limit + 1):
        leftBound = max(
            values[nextNumber]
            for nextNumber in removeBitMoves(number, "1")
        )
        zeroMoves = removeBitMoves(number, "0")
        rightBound = (
            min(values[nextNumber] for nextNumber in zeroMoves)
            if zeroMoves else None
        )
        values.append(simplestDyadicBetween(leftBound, rightBound))

    return values


def ceilFraction(value):
    return (value.numerator + value.denominator - 1) // value.denominator


def S(limit):
    values = gameValues(limit)
    total = sum(number * values[number] for number in range(1, limit + 1))
    return ceilFraction(total)


def solve():
    return S(TARGET_N)


def runTests():
    values = gameValues(10)
    assert values[2] == Fraction(1, 2)
    assert values[5] == Fraction(3, 2)
    assert values[10] == Fraction(3, 4)
    assert S(2) == 2
    assert S(5) == 17
    assert S(10) == 64
    assert solve() == 15800662276


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
