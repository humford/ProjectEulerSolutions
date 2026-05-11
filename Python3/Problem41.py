from itertools import permutations


def isPrime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    factor = 5
    step = 2
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += step
        step = 6 - step

    return True


def largestPandigitalPrime(maxDigits=9):
    for digits in range(maxDigits, 0, -1):
        if sum(range(1, digits + 1)) % 3 == 0:
            continue
        characters = "".join(str(value) for value in range(digits, 0, -1))
        for permutation in permutations(characters):
            candidate = int("".join(permutation))
            if isPrime(candidate):
                return candidate
    return None


def runTests():
    assert isPrime(2143)
    assert largestPandigitalPrime(4) == 4231


def solve():
    return largestPandigitalPrime()


if __name__ == "__main__":
    runTests()
    print(solve())
