import time
from functools import lru_cache


LIMIT = 10**18
CHOOSE = 10**12 - 10


def digitsInBase(number, base, length=0):
    digits = []

    while number > 0:
        digits.append(number % base)
        number //= base

    if not digits:
        digits.append(0)

    digits.extend([0] * max(0, length - len(digits)))
    return digits


def countNotDivisibleByPrime(limit, choose, prime):
    limitDigits = digitsInBase(limit - 1, prime)
    chooseDigits = digitsInBase(choose, prime, len(limitDigits))

    if len(chooseDigits) > len(limitDigits):
        return 0

    @lru_cache(None)
    def count(position, tight):
        if position < 0:
            return 1

        lower = chooseDigits[position]
        upper = limitDigits[position] if tight else prime - 1

        if lower > upper:
            return 0

        total = 0

        for digit in range(lower, upper + 1):
            total += count(position - 1, tight and digit == limitDigits[position])

        return total

    return count(len(limitDigits) - 1, True)


def lowBase5Values(choose, split):
    chooseDigits = digitsInBase(choose, 5, split)
    values = []

    def search(position, value, power):
        if position == split:
            values.append(value)
            return

        for digit in range(chooseDigits[position], 5):
            search(position + 1, value + digit * power, power * 5)

    search(0, 0, 1)
    return values


def countPowerOfTwoHighRange(low, step, mask, bits):
    forcedBits = mask.bit_length()

    @lru_cache(None)
    def count(bit, carry):
        if bit >= forcedBits:
            if bit < bits:
                return 1 << (bits - bit)

            return 1

        if bit < bits:
            total = 0

            for highBit in (0, 1):
                nextCarry = carry + highBit * step

                if ((mask >> bit) & 1) and not (nextCarry & 1):
                    continue

                total += count(bit + 1, nextCarry >> 1)

            return total

        if ((mask >> bit) & 1) and not (carry & 1):
            return 0

        return count(bit + 1, carry >> 1)

    return count(0, low)


def countHighRange(low, step, mask, count):
    total = 0
    offset = 0

    while count > 0:
        block = 1 << (count.bit_length() - 1)
        total += countPowerOfTwoHighRange(
            low + step * offset, step, mask, block.bit_length() - 1
        )
        offset += block
        count -= block

    return total


def countNotDivisibleBy2And5(limit, choose):
    split = len(digitsInBase(choose, 5))
    step = 5**split
    total = 0

    for low in lowBase5Values(choose, split):
        if low >= limit:
            continue

        highCount = (limit - 1 - low) // step + 1
        total += countHighRange(low, step, choose, highCount)

    return total


def binomialDivisibleBy10Count(limit=LIMIT, choose=CHOOSE):
    notDivisibleBy2 = countNotDivisibleByPrime(limit, choose, 2)
    notDivisibleBy5 = countNotDivisibleByPrime(limit, choose, 5)
    notDivisibleByBoth = countNotDivisibleBy2And5(limit, choose)

    return limit - choose - notDivisibleBy2 - notDivisibleBy5 + notDivisibleByBoth


def runTests():
    assert binomialDivisibleBy10Count(10**9, 10**7 - 10) == 989697000


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = binomialDivisibleBy10Count()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
