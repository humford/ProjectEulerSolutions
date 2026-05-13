import time
from collections import defaultdict
from itertools import combinations


LIMIT = 200_000


def smallestPrimeFactorSieve(limit):
    factors = list(range(limit + 1))

    for number in range(2, int(limit**0.5) + 1):
        if factors[number] != number:
            continue

        for multiple in range(number * number, limit + 1, number):
            if factors[multiple] == multiple:
                factors[multiple] = number

    return factors


def distinctPrimeFactors(number, smallestFactor):
    factors = []

    while number > 1:
        prime = smallestFactor[number]
        factors.append(prime)

        while number % prime == 0:
            number //= prime

    return tuple(factors)


def largestPrimePowers(limit, primes):
    powers = {}

    for prime in primes:
        power = prime

        while power * prime <= limit:
            power *= prime

        powers[prime] = power

    return powers


def positiveGainCandidates(limit):
    smallestFactor = smallestPrimeFactorSieve(limit)
    primes = [number for number in range(2, limit + 1) if smallestFactor[number] == number]
    primePowers = largestPrimePowers(limit, primes)
    bestByRadical = {}
    factorsByRadical = {}

    for number in range(2, limit + 1):
        factors = distinctPrimeFactors(number, smallestFactor)
        radical = 1

        for prime in factors:
            radical *= prime

        if number > bestByRadical.get(radical, 0):
            bestByRadical[radical] = number
            factorsByRadical[radical] = factors

    candidates = []

    for radical, value in bestByRadical.items():
        factors = factorsByRadical[radical]

        if len(factors) < 2:
            continue

        gain = value - sum(primePowers[prime] for prime in factors)

        if gain > 0:
            candidates.append((gain, factors, value))

    candidates.sort(reverse=True)

    return 1 + sum(primePowers.values()), candidates


def greedyPacking(candidates):
    usedPrimes = set()
    chosen = []

    for candidate in candidates:
        _gain, factors, _value = candidate

        if usedPrimes.isdisjoint(factors):
            usedPrimes.update(factors)
            chosen.append(candidate)

    return chosen


def improveByPairExchange(chosen, candidates):
    chosenKeys = {factors for _gain, factors, _value in chosen}
    usedBy = {
        prime: index
        for index, (_gain, factors, _value) in enumerate(chosen)
        for prime in factors
    }
    candidatesByConflict = defaultdict(list)

    for candidate in candidates:
        _gain, factors, _value = candidate

        if factors in chosenKeys:
            continue

        conflictMask = 0

        for prime in factors:
            if prime in usedBy:
                conflictMask |= 1 << usedBy[prime]

        if conflictMask:
            candidatesByConflict[conflictMask].append(candidate)

    bestDelta = 0
    bestRemoval = None
    bestAddition = None

    for first, second in combinations(range(len(chosen)), 2):
        removalMask = (1 << first) | (1 << second)
        removalCost = chosen[first][0] + chosen[second][0]
        exchangeCandidates = []
        submask = removalMask

        while submask:
            exchangeCandidates.extend(candidatesByConflict.get(submask, ()))
            submask = (submask - 1) & removalMask

        if not exchangeCandidates:
            continue

        exchangeCandidates.sort(reverse=True)

        if sum(candidate[0] for candidate in exchangeCandidates[:6]) <= (
            removalCost + bestDelta
        ):
            continue

        usedPrimes = set()
        addition = []
        additionGain = 0

        for candidate in exchangeCandidates:
            gain, factors, _value = candidate

            if usedPrimes.isdisjoint(factors):
                usedPrimes.update(factors)
                addition.append(candidate)
                additionGain += gain

        delta = additionGain - removalCost

        if delta > bestDelta:
            bestDelta = delta
            bestRemoval = {first, second}
            bestAddition = addition

    if bestDelta <= 0:
        return 0, chosen

    updated = [
        candidate
        for index, candidate in enumerate(chosen)
        if index not in bestRemoval
    ] + bestAddition
    updated.sort(reverse=True)

    return bestDelta, updated


def optimizedPacking(candidates):
    chosen = greedyPacking(candidates)

    while True:
        delta, chosen = improveByPairExchange(chosen, candidates)

        if delta == 0:
            return chosen


def coprimeSum(limit):
    baseline, candidates = positiveGainCandidates(limit)
    chosen = optimizedPacking(candidates)

    return baseline + sum(gain for gain, _factors, _value in chosen)


def exactCoprimeSum(limit):
    smallestFactor = smallestPrimeFactorSieve(limit)
    primes = [number for number in range(2, limit + 1) if smallestFactor[number] == number]
    primeIndex = {prime: index for index, prime in enumerate(primes)}
    bestByMask = {0: 1}

    for number in range(2, limit + 1):
        mask = 0

        for prime in distinctPrimeFactors(number, smallestFactor):
            mask |= 1 << primeIndex[prime]

        bestByMask[mask] = max(bestByMask.get(mask, 0), number)

    candidates = [(mask, value) for mask, value in bestByMask.items() if mask]
    dp = {0: 1}

    for mask, value in candidates:
        for usedMask, total in list(dp.items()):
            if usedMask & mask == 0:
                nextMask = usedMask | mask
                dp[nextMask] = max(dp.get(nextMask, 0), total + value)

    return max(dp.values())


def runTests():
    assert exactCoprimeSum(10) == 30
    assert exactCoprimeSum(30) == 193
    assert exactCoprimeSum(100) == 1356
    assert coprimeSum(10) == 30
    assert coprimeSum(30) == 193
    assert coprimeSum(100) == 1356


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = coprimeSum(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
