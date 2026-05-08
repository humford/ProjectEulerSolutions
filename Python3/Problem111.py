import itertools
import time


def isPrime(n):
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
    for prime in small_primes:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for base in (2, 3, 5, 7, 11):
        if base >= n:
            continue
        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def primesWithRepeatedDigit(length, digit, repeat_count):
    replacement_count = length - repeat_count
    repeated_digit = str(digit)
    replacement_digits = [str(value) for value in range(10) if value != digit]
    primes = []

    for positions in itertools.combinations(range(length), replacement_count):
        for replacements in itertools.product(replacement_digits, repeat=replacement_count):
            digits = [repeated_digit] * length
            for position, replacement in zip(positions, replacements):
                digits[position] = replacement

            if digits[0] == "0":
                continue

            number = int("".join(digits))
            if isPrime(number):
                primes.append(number)

    return primes


def repeatedDigitPrimeSum(length, digit):
    for repeat_count in range(length, -1, -1):
        primes = primesWithRepeatedDigit(length, digit, repeat_count)
        if primes:
            return sum(primes)
    return 0


def totalRepeatedDigitPrimeSum(length):
    return sum(repeatedDigitPrimeSum(length, digit) for digit in range(10))


def runTests():
    assert repeatedDigitPrimeSum(4, 0) == 67061


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totalRepeatedDigitPrimeSum(10)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
