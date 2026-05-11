def isPrime(n):
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    if n in small_primes:
        return True
    if any(n % prime == 0 for prime in small_primes):
        return False

    d = n - 1
    shifts = 0
    while d % 2 == 0:
        shifts += 1
        d //= 2

    for base in (2, 3, 5, 7, 11):
        if base >= n:
            continue
        value = pow(base, d, n)
        if value in (1, n - 1):
            continue
        for _ in range(shifts - 1):
            value = pow(value, 2, n)
            if value == n - 1:
                break
        else:
            return False

    return True


def spiralSideLengthBelowRatio(threshold):
    prime_count = 0
    diagonal_count = 1
    side_length = 1
    value = 1

    while True:
        side_length += 2
        step = side_length - 1
        for _ in range(4):
            value += step
            if isPrime(value):
                prime_count += 1
        diagonal_count += 4
        if prime_count / diagonal_count < threshold:
            return side_length


def runTests():
    assert spiralSideLengthBelowRatio(0.56) == 5


def solve():
    return spiralSideLengthBelowRatio(0.10)


if __name__ == "__main__":
    runTests()
    print(solve())
