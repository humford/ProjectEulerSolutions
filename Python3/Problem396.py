import time


LIMIT = 16
MODULUS = 10**9


def modulusChain(modulus):
    moduli = {modulus}
    changed = True

    while changed:
        changed = False

        for value in tuple(moduli):
            factor = value
            power = 0

            while factor and factor % 5 == 0:
                power += 1
                factor //= 5

            if power:
                exponentModulus = 4 * 5 ** (power - 1)

                if exponentModulus not in moduli:
                    moduli.add(exponentModulus)
                    changed = True

    return sorted(moduli)


MODULI = modulusChain(MODULUS)


def factorTwoFive(number):
    twos = 0

    while number and number % 2 == 0:
        twos += 1
        number //= 2

    fives = 0

    while number and number % 5 == 0:
        fives += 1
        number //= 5

    return twos, fives


def chineseRemainderForTwoFive(twoRemainder, twoPower, fiveRemainder, fivePower):
    if twoPower == 1:
        return fiveRemainder % fivePower
    if fivePower == 1:
        return twoRemainder % twoPower

    coefficient = ((fiveRemainder - twoRemainder) * pow(twoPower, -1, fivePower)) % fivePower
    return (twoRemainder + twoPower * coefficient) % (twoPower * fivePower)


def largePowerOfTwo(residues, modulus):
    if modulus == 1:
        return 0

    twos, fives = factorTwoFive(modulus)
    twoPower = 2**twos
    fivePower = 5**fives

    if fives:
        exponentModulus = 4 * 5 ** (fives - 1)
        exponent = (residues[exponentModulus] + 1) % exponentModulus
        fiveRemainder = pow(2, exponent, fivePower)
    else:
        fiveRemainder = 0

    if twos and fives:
        return chineseRemainderForTwoFive(0, twoPower, fiveRemainder, fivePower)
    if twos:
        return 0

    return fiveRemainder


def nextT2Residues(residues):
    nextResidues = {}

    for modulus in MODULI:
        nextResidues[modulus] = (
            largePowerOfTwo(residues, modulus)
            * ((residues[modulus] + 1) % modulus)
            - 1
        ) % modulus

    return nextResidues


def t2Exact(base):
    return (1 << (base + 1)) * (base + 1) - 1


def iterateT2(base, count):
    exact = base
    residues = None

    for _ in range(count):
        if residues is None and exact <= 1000:
            exact = t2Exact(exact)
        else:
            if residues is None:
                residues = {modulus: exact % modulus for modulus in MODULI}

            residues = nextT2Residues(residues)

    return exact % MODULUS if residues is None else residues[MODULUS]


def weakGoodsteinLength(number):
    base = 2

    if number & 1:
        base += 1
    if number & 2:
        base = 2 * base + 1
    if number & 4:
        base = t2Exact(base)
    if number & 8:
        base = iterateT2(base, base + 1)

    return (base - 2) % MODULUS


def weakGoodsteinSum(limit=LIMIT):
    return sum(weakGoodsteinLength(number) for number in range(1, limit)) % MODULUS


def runTests():
    assert weakGoodsteinLength(2) == 3
    assert weakGoodsteinLength(4) == 21
    assert weakGoodsteinLength(6) == 381
    assert weakGoodsteinSum(8) == 2517


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = weakGoodsteinSum()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
