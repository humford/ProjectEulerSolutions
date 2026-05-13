import time


P_TARGET = 2_000_000_011


def primeSieve(limit):
    if limit < 2:
        return []

    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for n in range(2, int(limit ** 0.5) + 1):
        if isPrime[n]:
            isPrime[n * n:limit + 1:n] = b"\x00" * (((limit - n * n) // n) + 1)

    return [n for n in range(2, limit + 1) if isPrime[n]]


def buildBestMap(primes, p, maxWeight):
    best = {}

    def search(index, residue, product, weight):
        if index == len(primes):
            current = best.get(residue)
            if current is None or weight < current[0] or (weight == current[0] and product < current[1]):
                best[residue] = (weight, product)
            return

        prime = primes[index]
        primeWeight = prime - 1
        maxExponent = (maxWeight - weight) // primeWeight

        nextResidue = residue
        nextProduct = product
        nextWeight = weight
        for _ in range(maxExponent + 1):
            search(index + 1, nextResidue, nextProduct, nextWeight)
            nextResidue = nextResidue * prime % p
            nextProduct *= prime
            nextWeight += primeWeight

    search(0, 1, 1, 0)
    return best


def buildTwoThreeStates(p, maxWeight):
    inverse2 = pow(2, p - 2, p)
    inverse3 = pow(3, p - 2, p)

    pow2Mod = [1] * (maxWeight + 1)
    pow2Int = [1] * (maxWeight + 1)
    inverse2Mod = [1] * (maxWeight + 1)
    for exponent in range(1, maxWeight + 1):
        pow2Mod[exponent] = pow2Mod[exponent - 1] * 2 % p
        pow2Int[exponent] = pow2Int[exponent - 1] * 2
        inverse2Mod[exponent] = inverse2Mod[exponent - 1] * inverse2 % p

    maxExponent3 = maxWeight // 2
    pow3Mod = [1] * (maxExponent3 + 1)
    pow3Int = [1] * (maxExponent3 + 1)
    inverse3Mod = [1] * (maxExponent3 + 1)
    for exponent in range(1, maxExponent3 + 1):
        pow3Mod[exponent] = pow3Mod[exponent - 1] * 3 % p
        pow3Int[exponent] = pow3Int[exponent - 1] * 3
        inverse3Mod[exponent] = inverse3Mod[exponent - 1] * inverse3 % p

    states = []
    for exponent3 in range(maxExponent3 + 1):
        weight3 = 2 * exponent3
        remaining = maxWeight - weight3
        for exponent2 in range(remaining + 1):
            weight = weight3 + exponent2
            residue = pow3Mod[exponent3] * pow2Mod[exponent2] % p
            product = pow3Int[exponent3] * pow2Int[exponent2]
            inverseResidue = inverse3Mod[exponent3] * inverse2Mod[exponent2] % p
            states.append((weight, residue, product, inverseResidue))

    states.sort()
    return states


def searchWithBound(p, maxWeight):
    primes = primeSieve(maxWeight + 1)
    smallPrimes = [prime for prime in primes if 5 <= prime <= 23]
    largePrimes = [prime for prime in primes if prime >= 29]

    bestSmall = buildBestMap(smallPrimes, p, maxWeight)
    bestLarge = buildBestMap(largePrimes, p, maxWeight)

    largeStates = []
    for residue, (weight, product) in bestLarge.items():
        largeStates.append((weight, residue, product, pow(residue, p - 2, p)))
    largeStates.sort()

    twoThreeStates = buildTwoThreeStates(p, maxWeight)
    target = p - 1
    bestWeight = None
    bestProduct = None

    for largeWeight, _, largeProduct, largeInverse in largeStates:
        if largeWeight > maxWeight:
            break

        neededBase = target * largeInverse % p
        maxTwoThreeWeight = maxWeight - largeWeight

        for twoThreeWeight, _, twoThreeProduct, twoThreeInverse in twoThreeStates:
            if twoThreeWeight > maxTwoThreeWeight:
                break

            remaining = maxWeight - largeWeight - twoThreeWeight
            neededSmall = neededBase * twoThreeInverse % p
            smallEntry = bestSmall.get(neededSmall)
            if smallEntry is None:
                continue

            smallWeight, smallProduct = smallEntry
            if smallWeight > remaining:
                continue

            totalWeight = largeWeight + twoThreeWeight + smallWeight
            product = largeProduct * twoThreeProduct * smallProduct
            if (
                bestWeight is None
                or totalWeight < bestWeight
                or (totalWeight == bestWeight and product < bestProduct)
            ):
                bestWeight = totalWeight
                bestProduct = product

    return bestProduct


def solve(p):
    for maxWeight in (240, 260, 280, 300, 320, 360, 400):
        product = searchWithBound(p, maxWeight)
        if product is not None:
            return product

    maxWeight = 440
    while True:
        product = searchWithBound(p, maxWeight)
        if product is not None:
            return product
        maxWeight += 40


def runTests():
    assert solve(5) == 4


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve(P_TARGET)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
