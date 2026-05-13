import bisect
import math
import time


MODULUS = 2 ** 32


def generateHammingNumbers(limit):
    numbers = []
    powerOfTwo = 1
    while powerOfTwo <= limit:
        powerOfThree = powerOfTwo
        while powerOfThree <= limit:
            value = powerOfThree
            while value <= limit:
                numbers.append(value)
                value *= 5
            powerOfThree *= 3
        powerOfTwo *= 2
    return sorted(numbers)


def isPrime(number):
    if number < 2:
        return False

    testPrimes = (2, 3, 5, 7, 11, 13, 17)
    for prime in testPrimes:
        if number % prime == 0:
            return number == prime

    oddPart = number - 1
    shift = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        shift += 1

    for base in testPrimes:
        value = pow(base, oddPart, number)
        if value == 1 or value == number - 1:
            continue

        for _ in range(shift - 1):
            value = value * value % number
            if value == number - 1:
                break
        else:
            return False

    return True


def phi(number):
    result = number
    value = number
    factor = 2
    while factor * factor <= value:
        if value % factor == 0:
            while value % factor == 0:
                value //= factor
            result -= result // factor
        factor += 1 if factor == 2 else 2
    if value > 1:
        result -= result // value
    return result


def isHamming(number):
    for factor in (2, 3, 5):
        while number % factor == 0:
            number //= factor
    return number == 1


def bruteHammingTotientSum(limit):
    return sum(number for number in range(1, limit + 1) if isHamming(phi(number)))


def hammingTotientSum(limit):
    hammingNumbers = generateHammingNumbers(limit)
    prefixSums = [0]
    for number in hammingNumbers:
        prefixSums.append((prefixSums[-1] + number) % MODULUS)

    hammingPrimes = [
        number + 1
        for number in hammingNumbers
        if number + 1 > 5 and number + 1 <= limit and isPrime(number + 1)
    ]

    def hammingSumUpTo(bound):
        return prefixSums[bisect.bisect_right(hammingNumbers, bound)]

    def search(startIndex, squarefreePart):
        total = squarefreePart * hammingSumUpTo(limit // squarefreePart)
        total %= MODULUS

        for index in range(startIndex, len(hammingPrimes)):
            nextPart = squarefreePart * hammingPrimes[index]
            if nextPart > limit:
                break
            total += search(index + 1, nextPart)
            total %= MODULUS

        return total

    # If phi(n) is 5-smooth, every prime factor of n is either 2, 3, 5, or a
    # prime p with p - 1 Hamming.  Such p > 5 can appear only to the first
    # power, while the remaining 2/3/5 part can be any Hamming number.
    return search(0, 1)


def runTests():
    assert bruteHammingTotientSum(100) == 3_728
    assert hammingTotientSum(100) == 3_728
    assert hammingTotientSum(1_000) == bruteHammingTotientSum(1_000)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = hammingTotientSum(10 ** 12)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
