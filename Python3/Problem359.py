import time


NUMBER = 71328803586048
MODULUS = 10**8


def hotelGuest(floor, room, modulus=None):
    result = ((floor + 1) // 2) * floor

    if floor % 2 == 1 and floor > 1:
        result -= (floor + 1) // 2

    evenIncrement = 1 if floor % 2 == 1 else 2 * floor + 1
    oddIncrement = 2 * floor if floor % 2 == 1 else 2

    if floor == 1:
        oddIncrement = 3
        evenIncrement = 2

    evenRooms = room // 2
    oddRooms = (room - 1) // 2
    result += evenRooms * (evenIncrement - 2) + evenRooms * (evenRooms + 1)
    result += oddRooms * (oddIncrement - 2) + oddRooms * (oddRooms + 1)

    if modulus is not None:
        return result % modulus

    return result


def hilbertHotelSum():
    total = 0

    for power2 in range(28):
        for power3 in range(13):
            floor = (2**power2) * (3**power3)
            total = (total + hotelGuest(floor, NUMBER // floor, MODULUS)) % MODULUS

    return total


def runTests():
    assert hotelGuest(1, 1) == 1
    assert hotelGuest(1, 2) == 3
    assert hotelGuest(2, 1) == 2
    assert hotelGuest(10, 20) == 440
    assert hotelGuest(25, 75) == 4863
    assert hotelGuest(99, 100) == 19454


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hilbertHotelSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
