import sys
import time
from math import factorial


MODULUS = 83_456_729
TARGET_N = 34


def primeSieve(limit):
    isPrime = [True] * (limit + 1)
    isPrime[0:2] = [False, False]

    for value in range(2, int(limit**0.5) + 1):
        if isPrime[value]:
            for multiple in range(value * value, limit + 1, value):
                isPrime[multiple] = False

    return [value for value in range(2, limit + 1) if isPrime[value]]


def relevantOddPrimes(evens, primes):
    relevant = set()

    for value in evens:
        for prime in primes:
            if prime == 2:
                continue
            if value % prime == 0:
                relevant.add(prime)

    return sorted(relevant)


def maskCounts(values, primes):
    primeToBit = {prime: index for index, prime in enumerate(primes)}
    counts = {}

    for value in values:
        mask = 0
        for prime in primes:
            if value % prime == 0:
                mask |= 1 << primeToBit[prime]
        counts[mask] = counts.get(mask, 0) + 1

    masks = sorted(counts)
    return masks, [counts[mask] for mask in masks]


def mixedRadixTables(counts):
    multipliers = []
    totalStates = 1

    for count in counts:
        multipliers.append(totalStates)
        totalStates *= count + 1

    decrement = [[-1] * len(counts) for _ in range(totalStates)]
    remaining = [0] * totalStates

    for state in range(totalStates):
        for index, (count, multiplier) in enumerate(zip(counts, multipliers)):
            digit = (state // multiplier) % (count + 1)
            remaining[state] += digit
            if digit:
                decrement[state][index] = state - multiplier

    initial = sum(
        count * multiplier
        for count, multiplier in zip(counts, multipliers)
    )

    return decrement, remaining, initial, totalStates


def countAlternatingSequences(evenMasks, evenCounts, oddMasks, oddCounts):
    evenDecrement, evenRemaining, evenInitial, evenStates = mixedRadixTables(evenCounts)
    oddDecrement, oddRemaining, oddInitial, oddStates = mixedRadixTables(oddCounts)

    evenToOdd = [
        [index for index, oddMask in enumerate(oddMasks) if evenMask & oddMask == 0]
        for evenMask in evenMasks
    ]
    oddToEven = [
        [index for index, evenMask in enumerate(evenMasks) if evenMask & oddMask == 0]
        for oddMask in oddMasks
    ]

    evenMemo = {}
    oddMemo = {}

    def evenStep(lastEven, evenState, oddState):
        if evenRemaining[evenState] == 0 and oddRemaining[oddState] == 0:
            return 1
        if oddRemaining[oddState] == 0:
            return 0

        key = (evenState * oddStates + oddState) * len(evenMasks) + lastEven
        if key in evenMemo:
            return evenMemo[key]

        total = 0
        for oddIndex in evenToOdd[lastEven]:
            nextOddState = oddDecrement[oddState][oddIndex]
            if nextOddState != -1:
                total += oddStep(oddIndex, evenState, nextOddState)
        total %= MODULUS
        evenMemo[key] = total
        return total

    def oddStep(lastOdd, evenState, oddState):
        if evenRemaining[evenState] == 0 and oddRemaining[oddState] == 0:
            return 1
        if evenRemaining[evenState] == 0:
            return 0

        key = (evenState * oddStates + oddState) * len(oddMasks) + lastOdd
        if key in oddMemo:
            return oddMemo[key]

        total = 0
        for evenIndex in oddToEven[lastOdd]:
            nextEvenState = evenDecrement[evenState][evenIndex]
            if nextEvenState != -1:
                total += evenStep(evenIndex, nextEvenState, oddState)
        total %= MODULUS
        oddMemo[key] = total
        return total

    total = 0
    for evenIndex in range(len(evenMasks)):
        nextEvenState = evenDecrement[evenInitial][evenIndex]
        if nextEvenState != -1:
            total += evenStep(evenIndex, nextEvenState, oddInitial)

    return total % MODULUS


def P(limit):
    values = list(range(2, limit + 1))
    evens = [value for value in values if value % 2 == 0]
    odds = [value for value in values if value % 2 == 1]

    if len(evens) != len(odds) + 1:
        raise ValueError("this implementation expects one more even than odd")

    primes = primeSieve(limit)
    relevantPrimes = relevantOddPrimes(evens, primes)
    evenMasks, evenCounts = maskCounts(evens, relevantPrimes)
    oddMasks, oddCounts = maskCounts(odds, relevantPrimes)

    typeSequenceCount = countAlternatingSequences(
        evenMasks,
        evenCounts,
        oddMasks,
        oddCounts,
    )

    labeledCount = typeSequenceCount
    for count in evenCounts + oddCounts:
        labeledCount = labeledCount * factorial(count) % MODULUS

    return labeledCount


def solve():
    return P(TARGET_N)


def runTests():
    assert P(4) == 2
    assert P(10) == 576


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    runTests()
    start = time.time()
    answer = solve()
    assert answer == 5570163
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
