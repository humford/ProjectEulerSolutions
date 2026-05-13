import time


MULTIPLIER = 1_504_170_715_041_707
MODULUS = 4_503_599_627_370_517
FORWARD_STOP = 20_000_000


def eulercoinTerm(index):
    return MULTIPLIER * index % MODULUS


def eulercoinSum():
    # Search down from the sequence side, then up through candidate values using
    # the modular inverse once the remaining value range is small.
    forwardCoins, limit = forwardEulercoins()
    return sum(forwardCoins) + sum(reverseEulercoinsBelow(limit))


def firstEulercoins(count):
    coins = [MULTIPLIER]
    lowest = MULTIPLIER
    value = MULTIPLIER

    while len(coins) < count:
        value = (value + MULTIPLIER) % MODULUS
        if value < lowest:
            lowest = value
            coins.append(value)

    return coins


def forwardEulercoins(stopBelow=FORWARD_STOP):
    coins = [MULTIPLIER]
    lowest = MULTIPLIER
    value = MULTIPLIER

    while lowest >= stopBelow:
        value = (value + MULTIPLIER) % MODULUS
        if value < lowest:
            lowest = value
            coins.append(value)

    return coins, lowest


def reverseEulercoinsBelow(limit):
    inverseMultiplier = pow(MULTIPLIER, -1, MODULUS)
    bestIndex = MODULUS
    coins = []

    for coin in range(1, limit):
        index = (coin * inverseMultiplier) % MODULUS
        if index < bestIndex:
            bestIndex = index
            coins.append(coin)

    return coins


def runTests():
    assert eulercoinTerm(1) == 1_504_170_715_041_707
    assert eulercoinTerm(2) == 3_008_341_430_083_414
    assert eulercoinTerm(3) == 8_912_517_754_604
    assert sum(firstEulercoins(2)) == 1_513_083_232_796_311


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = eulercoinSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
