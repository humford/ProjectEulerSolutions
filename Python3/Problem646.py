import bisect
import time


MODULUS = 1_000_000_007


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)
    return [number for number, isPrime in enumerate(sieve) if isPrime]


def factorialFactorization(limit):
    factors = []
    for prime in primesUpTo(limit):
        exponent = 0
        power = prime
        while power <= limit:
            exponent += limit // power
            power *= prime
        factors.append((prime, exponent))
    return factors


def generateDivisorEntries(factors, upper, modulus):
    entries = []

    def walk(index, value, valueMod, parity):
        if value > upper:
            return
        if index == len(factors):
            if modulus is None:
                signedValue = -value if parity else value
            else:
                signedValue = (-valueMod) % modulus if parity else valueMod
            entries.append((value, signedValue))
            return

        prime, exponent = factors[index]
        nextValue = value
        nextValueMod = valueMod
        for extraExponent in range(exponent + 1):
            walk(index + 1, nextValue, nextValueMod, parity ^ (extraExponent & 1))
            nextValue *= prime
            if nextValue > upper:
                break
            nextValueMod = nextValueMod * prime if modulus is None else nextValueMod * prime % modulus

    walk(0, 1, 1, 0)
    return entries


def boundedLiouvilleDivisorSum(factorialArgument, lower, upper, modulus=None):
    factors = factorialFactorization(factorialArgument)
    split = min(5, len(factors))
    leftFactors = factors[:split]
    rightFactors = factors[split:]

    rightEntries = generateDivisorEntries(rightFactors, upper, modulus)
    rightEntries.sort()
    rightValues = [value for value, _ in rightEntries]
    prefixSums = [0]
    running = 0
    for _, signedValue in rightEntries:
        running += signedValue
        if modulus is not None:
            running %= modulus
        prefixSums.append(running)

    total = 0

    def walkLeft(index, value, valueMod, parity):
        nonlocal total
        if value > upper:
            return
        if index == len(leftFactors):
            lowerBound = (lower + value - 1) // value
            upperBound = upper // value
            start = bisect.bisect_left(rightValues, lowerBound)
            end = bisect.bisect_right(rightValues, upperBound)
            rightSum = prefixSums[end] - prefixSums[start]
            if modulus is not None:
                rightSum %= modulus
                signedLeft = (-valueMod) % modulus if parity else valueMod
                total = (total + signedLeft * rightSum) % modulus
            else:
                signedLeft = -value if parity else value
                total += signedLeft * rightSum
            return

        prime, exponent = leftFactors[index]
        nextValue = value
        nextValueMod = valueMod
        for extraExponent in range(exponent + 1):
            walkLeft(index + 1, nextValue, nextValueMod, parity ^ (extraExponent & 1))
            nextValue *= prime
            if nextValue > upper:
                break
            nextValueMod = nextValueMod * prime if modulus is None else nextValueMod * prime % modulus

    walkLeft(0, 1, 1, 0)
    return total % modulus if modulus is not None else total


def runTests():
    assert boundedLiouvilleDivisorSum(10, 100, 1_000) == 1_457
    assert boundedLiouvilleDivisorSum(15, 10 ** 3, 10 ** 5) == -107_974
    assert boundedLiouvilleDivisorSum(30, 10 ** 8, 10 ** 12) == 9_766_732_243_224


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = boundedLiouvilleDivisorSum(70, 10 ** 20, 10 ** 60, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
