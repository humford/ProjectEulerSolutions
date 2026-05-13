import time


PRIMES_UP_TO_47 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
STORMER_BOUND_47 = 1_109_496_723_126


def isSmooth(number, limit):
    for prime in PRIMES_UP_TO_47:
        if prime > limit:
            break
        while number % prime == 0:
            number //= prime
    return number == 1


def smoothNumbers(limit, primes=PRIMES_UP_TO_47):
    numbers = []

    def generate(index, value):
        if index == len(primes):
            numbers.append(value)
            return

        prime = primes[index]
        while value <= limit:
            generate(index + 1, value)
            value *= prime

    generate(0, 1)
    numbers.sort()
    return numbers


def smoothTriangularIndices():
    smooths = smoothNumbers(STORMER_BOUND_47)
    return [
        current
        for current, nextValue in zip(smooths, smooths[1:])
        if nextValue == current + 1
    ]


def smoothTriangularIndexSum():
    return sum(smoothTriangularIndices())


def runTests():
    assert isSmooth(1, 47)
    assert isSmooth(360, 47)
    assert not isSmooth(53, 47)

    tinySmooths = smoothNumbers(100, [2, 3, 5])
    tinyIndices = [
        current
        for current, nextValue in zip(tinySmooths, tinySmooths[1:])
        if nextValue == current + 1
    ]
    assert tinyIndices == [1, 2, 3, 4, 5, 8, 9, 15, 24, 80]


if __name__ == "__main__":
    runTests()
    start = time.time()
    indices = smoothTriangularIndices()
    answer = sum(indices)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
