import time


MOD = 10 ** 15


def crt(residueA, modulusA, residueB, modulusB):
    adjustment = (residueB - residueA) % modulusB
    multiplier = adjustment * pow(modulusA, -1, modulusB) % modulusB
    return (residueA + modulusA * multiplier) % (modulusA * modulusB)


def factorTwoFive(n):
    twos = 0
    while n % 2 == 0:
        twos += 1
        n //= 2

    fives = 0
    while n % 5 == 0:
        fives += 1
        n //= 5

    return twos, fives, n


def phiTwoFive(n):
    twos, fives, remainder = factorTwoFive(n)
    if remainder != 1:
        raise ValueError("Expected only factors 2 and 5")

    result = n
    if twos:
        result //= 2
    if fives:
        result = result // 5 * 4

    return result


def totientChainLength(n):
    length = 0
    while n != 1:
        n = phiTwoFive(n)
        length += 1
    return length


def cappedTetration(height, cap):
    value = 2
    if height <= 1:
        return min(value, cap)

    for _ in range(2, height + 1):
        if value >= 60:
            return cap
        value = 1 << value
        if value >= cap:
            return cap

    return value


def tetrationModPowerOfTwo(height, exponent):
    if exponent <= 0:
        return 0
    modulus = 1 << exponent
    if height == 1:
        return 2 % modulus

    towerExponent = cappedTetration(height - 1, exponent)
    if towerExponent >= exponent:
        return 0
    return (1 << towerExponent) % modulus


def tetrationMod(height, modulus):
    if modulus == 1:
        return 0

    twos, fives, remainder = factorTwoFive(modulus)
    if remainder != 1:
        raise ValueError("Expected only factors 2 and 5")

    if fives == 0:
        return tetrationModPowerOfTwo(height, twos)

    if twos == 0:
        if height == 1:
            return 2 % modulus
        return pow(2, tetrationMod(height - 1, phiTwoFive(modulus)), modulus)

    modulusTwo = 1 << twos
    modulusFive = 5 ** fives
    residueTwo = tetrationModPowerOfTwo(height, twos)
    residueFive = tetrationMod(height, modulusFive)

    return crt(residueTwo, modulusTwo, residueFive, modulusFive)


def stableTetrationMod(modulus):
    height = totientChainLength(modulus) + 1
    return tetrationMod(height, modulus)


def smallAckermann(m, n):
    if m == 0:
        return n + 1
    if m == 1:
        return n + 2
    if m == 2:
        return 2 * n + 3
    if m == 3:
        return (1 << (n + 3)) - 3
    if m == 4:
        value = smallAckermann(3, 1)
        for _ in range(n):
            value = (1 << (value + 3)) - 3
        return value
    if m == 5 and n == 0:
        return smallAckermann(4, 1)

    raise ValueError("Small Ackermann helper was called outside its intended range")


def f13Over10Example():
    value = 7
    for _ in range(25):
        value = 3 * value + 4
    return value


def f22Over7Mod():
    modulusTwo = 1 << 15
    modulusFive = 5 ** 15

    residueTwo = (-3) % modulusTwo
    residueFive = (stableTetrationMod(modulusFive) - 3) % modulusFive

    return crt(residueTwo, modulusTwo, residueFive, modulusFive)


def runTests():
    assert smallAckermann(1, 1) == 3
    assert smallAckermann(5, 0) == 65_533
    assert f13Over10Example() == 7_625_597_484_985


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = f22Over7Mod()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
