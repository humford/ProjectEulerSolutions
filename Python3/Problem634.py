import math
import time


def integerRoot(limit, exponent):
    root = int(limit ** (1 / exponent)) + 2
    while root ** exponent > limit:
        root -= 1
    while (root + 1) ** exponent <= limit:
        root += 1
    return root


def mobiusUpTo(limit):
    mobius = [0] * (limit + 1)
    mobius[1] = 1
    primes = []
    isComposite = [False] * (limit + 1)

    for number in range(2, limit + 1):
        if not isComposite[number]:
            primes.append(number)
            mobius[number] = -1
        for prime in primes:
            multiple = number * prime
            if multiple > limit:
                break
            isComposite[multiple] = True
            if number % prime == 0:
                mobius[multiple] = 0
                break
            mobius[multiple] = -mobius[number]

    return mobius


def primesUpTo(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if sieve[number]:
            start = number * number
            sieve[start : limit + 1 : number] = b"\x00" * (((limit - start) // number) + 1)
    return [number for number, isPrime in enumerate(sieve) if isPrime]


def squarefreeCount(limit):
    mobius = mobiusUpTo(math.isqrt(limit))
    return sum(mobius[divisor] * (limit // (divisor * divisor)) for divisor in range(1, len(mobius)))


def cubefreeCount(limit):
    root = integerRoot(limit, 3)
    mobius = mobiusUpTo(root)
    return sum(mobius[divisor] * (limit // (divisor ** 3)) for divisor in range(1, root + 1))


def powerfulCount(limit):
    cubeRoot = integerRoot(limit, 3)
    mobius = mobiusUpTo(cubeRoot)
    total = 0
    for cubePart in range(1, cubeRoot + 1):
        if mobius[cubePart] != 0:
            total += math.isqrt(limit // (cubePart ** 3))
    return total - 1


def primeSixthPowerCount(limit):
    return len(primesUpTo(integerRoot(limit, 6)))


def formCount(limit):
    return (
        powerfulCount(limit)
        - (cubefreeCount(math.isqrt(limit)) - 1)
        - (squarefreeCount(integerRoot(limit, 3)) - 1)
        - primeSixthPowerCount(limit)
    )


def formCountBrute(limit):
    values = set()
    base = 2
    while base * base * 8 <= limit:
        square = base * base
        cubeBase = 2
        while square * cubeBase ** 3 <= limit:
            values.add(square * cubeBase ** 3)
            cubeBase += 1
        base += 1
    return len(values)


def runTests():
    assert formCountBrute(100) == 2
    assert formCountBrute(20_000) == 130
    assert formCount(100) == 2
    assert formCount(20_000) == 130
    assert formCount(3 * 10 ** 6) == 2_014


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = formCount(9 * 10 ** 18)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
