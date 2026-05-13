import functools
import time


MODULUS = 100000007
TARGET = 1000000


def seatPriority(mask, seat, seats):
    leftOccupied = seat > 0 and bool(mask & (1 << (seat - 1)))
    rightOccupied = seat + 1 < seats and bool(mask & (1 << (seat + 1)))
    occupiedAdjacent = leftOccupied + rightOccupied

    if occupiedAdjacent == 0:
        return 1

    if occupiedAdjacent == 1:
        return 2

    return 3


def exactSeatingCount(seats):
    fullMask = (1 << seats) - 1

    @functools.lru_cache(None)
    def count(mask):
        if mask == fullMask:
            return 1

        choices = []
        bestPriority = 4

        for seat in range(seats):
            if mask & (1 << seat):
                continue

            priority = seatPriority(mask, seat, seats)

            if priority < bestPriority:
                bestPriority = priority
                choices = [seat]
            elif priority == bestPriority:
                choices.append(seat)

        return sum(count(mask | (1 << seat)) for seat in choices)

    return count(0)


def precomputeFactorials(limit, modulus):
    factorials = [1] * (limit + 1)
    powersOfTwo = [1] * (limit + 1)

    for number in range(1, limit + 1):
        factorials[number] = factorials[number - 1] * number % modulus
        powersOfTwo[number] = powersOfTwo[number - 1] * 2 % modulus

    inverseFactorials = [1] * (limit + 1)
    inverseFactorials[limit] = pow(factorials[limit], -1, modulus)
    for number in range(limit, 0, -1):
        inverseFactorials[number - 1] = inverseFactorials[number] * number % modulus

    return factorials, inverseFactorials, powersOfTwo


def combination(number, choose, factorials, inverseFactorials, modulus):
    if choose < 0 or choose > number:
        return 0

    return (
        factorials[number]
        * inverseFactorials[choose]
        * inverseFactorials[number - choose]
        % modulus
    )


def comfortableDistanceCount(seats, modulus=MODULUS):
    factorials, inverseFactorials, powersOfTwo = precomputeFactorials(seats, modulus)
    total = 0

    for edgeGapCount in range(3):
        firstInitialSeat = max(1, (seats + 4 - edgeGapCount) // 3)
        lastInitialSeat = (seats + 1 - edgeGapCount) // 2

        for initialSeatCount in range(firstInitialSeat, lastInitialSeat + 1):
            doubleGapCount = seats - (2 * initialSeatCount - 1) - edgeGapCount
            edgeChoices = 1 if edgeGapCount != 1 else 2
            gapChoices = combination(
                initialSeatCount - 1,
                doubleGapCount,
                factorials,
                inverseFactorials,
                modulus,
            )
            term = edgeChoices * gapChoices % modulus
            term = term * factorials[initialSeatCount] % modulus
            term = term * factorials[doubleGapCount + edgeGapCount] % modulus
            term = term * powersOfTwo[doubleGapCount] % modulus
            term = term * factorials[initialSeatCount - 1] % modulus
            total = (total + term) % modulus

    return total


def runTests():
    assert exactSeatingCount(4) == 8
    assert exactSeatingCount(10) == 61632
    assert comfortableDistanceCount(4) == 8
    assert comfortableDistanceCount(10) == 61632
    assert comfortableDistanceCount(1000) == 47255094


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = comfortableDistanceCount(TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
