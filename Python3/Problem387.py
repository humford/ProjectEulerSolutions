import time


LIMIT = 10**14


def isPrime(number):
    if number < 2:
        return False

    smallPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    for prime in smallPrimes:
        if number % prime == 0:
            return number == prime

    oddPart = number - 1
    shift = 0

    while oddPart % 2 == 0:
        shift += 1
        oddPart //= 2

    for base in [2, 3, 5, 7, 11, 13]:
        if base >= number:
            continue

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


def harshadPrimeSum(limit=LIMIT):
    total = 0
    stack = [(digit, digit) for digit in range(1, 10)]

    while stack:
        number, digitSum = stack.pop()

        if number >= limit:
            continue

        if number % digitSum == 0:
            if isPrime(number // digitSum):
                for digit in [1, 3, 7, 9]:
                    candidate = 10 * number + digit

                    if candidate < limit and isPrime(candidate):
                        total += candidate

            for digit in range(10):
                nextNumber = 10 * number + digit
                nextDigitSum = digitSum + digit

                if nextNumber < limit and nextNumber % nextDigitSum == 0:
                    stack.append((nextNumber, nextDigitSum))

    return total


def runTests():
    assert harshadPrimeSum(10000) == 90619


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = harshadPrimeSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
