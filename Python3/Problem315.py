import time


LOWER_LIMIT = 10**7
UPPER_LIMIT = 2 * 10**7

DIGIT_MASKS = [
    0b1110111,
    0b0100100,
    0b1011101,
    0b1101101,
    0b0101110,
    0b1101011,
    0b1111011,
    0b0100111,
    0b1111111,
    0b1101111,
]
DIGIT_COUNTS = [mask.bit_count() for mask in DIGIT_MASKS]


def primeSieve(limit):
    sieve = bytearray(b"\x01") * limit
    sieve[0] = 0
    sieve[1] = 0

    for number in range(4, limit, 2):
        sieve[number] = 0

    for number in range(3, int((limit - 1) ** 0.5) + 1, 2):
        if sieve[number]:
            start = number * number
            step = 2 * number
            sieve[start::step] = b"\x00" * ((limit - 1 - start) // step + 1)

    return sieve


def digits(number):
    return [int(digit) for digit in str(number)]


def digitSum(numberDigits):
    return sum(numberDigits)


def digitalRootChain(number):
    chain = [digits(number)]

    while len(chain[-1]) > 1:
        chain.append(digits(digitSum(chain[-1])))

    return chain


def displayCost(numberDigits):
    return sum(DIGIT_COUNTS[digit] for digit in numberDigits)


def transitionCost(fromDigits, toDigits):
    total = 0
    length = max(len(fromDigits), len(toDigits))

    for index in range(1, length + 1):
        fromMask = DIGIT_MASKS[fromDigits[-index]] if index <= len(fromDigits) else 0
        toMask = DIGIT_MASKS[toDigits[-index]] if index <= len(toDigits) else 0
        total += (fromMask ^ toMask).bit_count()

    return total


def samClockTransitions(number):
    return sum(2 * displayCost(numberDigits) for numberDigits in digitalRootChain(number))


def maxClockTransitions(number):
    chain = digitalRootChain(number)
    total = displayCost(chain[0])

    for previous, current in zip(chain, chain[1:]):
        total += transitionCost(previous, current)

    total += displayCost(chain[-1])
    return total


def clockTransitionDifference(lower=LOWER_LIMIT, upper=UPPER_LIMIT):
    primes = primeSieve(upper)
    total = 0

    for prime in range(lower, upper):
        if primes[prime]:
            total += samClockTransitions(prime) - maxClockTransitions(prime)

    return total


def runTests():
    assert samClockTransitions(137) == 40
    assert maxClockTransitions(137) == 30


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = clockTransitionDifference()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
