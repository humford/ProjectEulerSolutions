from math import gcd
import time


PROBLEM_N = 350


def lcm(left, right):
    return left // gcd(left, right) * right


def primeSieve(limit):
    if limit < 2:
        return []

    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"
    for value in range(2, int(limit**0.5) + 1):
        if isPrime[value]:
            for multiple in range(value * value, limit + 1, value):
                isPrime[multiple] = 0
    return [
        value for value in range(2, limit + 1)
        if isPrime[value]
    ]


def scientificFormat(value):
    mantissa, exponent = format(value, ".9e").split("e")
    return mantissa + "e" + str(int(exponent))


def averageOrderSquare(n):
    if n == 0:
        return 1.0

    primePowerExtractors = [[] for _ in range(n + 1)]
    for prime in primeSieve(n):
        power = prime
        while power <= n:
            primePowerExtractors[power].append(prime)
            power *= prime

    states = [dict() for _ in range(n + 1)]
    states[0][1] = 1.0

    for cycleLength in range(n, 0, -1):
        nextStates = [dict() for _ in range(n + 1)]
        inverseCycleLength = 1.0 / cycleLength

        for used in range(n + 1):
            current = states[used]
            if not current:
                continue
            maxMultiplicity = (n - used) // cycleLength

            for trackedLcm, contribution in current.items():
                nextStates[used][trackedLcm] = (
                    nextStates[used].get(trackedLcm, 0.0) + contribution
                )

                if maxMultiplicity == 0:
                    continue

                updatedLcm = lcm(trackedLcm, cycleLength)
                term = contribution * inverseCycleLength
                nextUsed = used + cycleLength
                nextStates[nextUsed][updatedLcm] = (
                    nextStates[nextUsed].get(updatedLcm, 0.0) + term
                )

                for multiplicity in range(2, maxMultiplicity + 1):
                    term /= multiplicity * cycleLength
                    nextUsed += cycleLength
                    nextStates[nextUsed][updatedLcm] = (
                        nextStates[nextUsed].get(updatedLcm, 0.0) + term
                    )

        if primePowerExtractors[cycleLength]:
            compressed = [dict() for _ in range(n + 1)]
            for used in range(n + 1):
                current = nextStates[used]
                if not current:
                    continue
                for trackedLcm, contribution in current.items():
                    reducedLcm = trackedLcm
                    value = contribution
                    for prime in primePowerExtractors[cycleLength]:
                        if reducedLcm % cycleLength == 0:
                            reducedLcm //= prime
                            value *= prime * prime
                    compressed[used][reducedLcm] = (
                        compressed[used].get(reducedLcm, 0.0) + value
                    )
            nextStates = compressed

        states = nextStates

    return states[n].get(1, 0.0)


def runTests():
    assert scientificFormat(averageOrderSquare(3)) == "5.166666667e0"
    assert scientificFormat(averageOrderSquare(5)) == "1.734166667e1"
    assert scientificFormat(averageOrderSquare(20)) == "5.106136147e3"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = scientificFormat(averageOrderSquare(PROBLEM_N))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
