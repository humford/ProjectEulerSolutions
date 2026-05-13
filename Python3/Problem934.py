import time


TARGET = 10**17


def primeGenerator():
    primes = []
    candidate = 2

    while True:
        isPrime = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                isPrime = False
                break

        if isPrime:
            primes.append(candidate)
            yield candidate

        candidate += 1 if candidate == 2 else 2


def allowedResidues(prime):
    return tuple(range(0, prime, 7))


def combineResidue(residue, modulus, targetResidue, prime, inverseModulus):
    multiplier = (targetResidue - residue) * inverseModulus % prime
    return residue + modulus * multiplier


def residueCount(residues, modulus, limit):
    total = 0

    for residue in residues:
        if residue == 0:
            total += limit // modulus
        elif residue <= limit:
            total += (limit - residue) // modulus + 1

    return total


def unluckyPrime(n):
    for prime in primeGenerator():
        if n % prime not in allowedResidues(prime):
            return prime


def U(limit):
    answer = 0
    previousSurvivors = limit
    residues = [0]
    modulus = 1
    actualNumbers = None

    for prime in primeGenerator():
        allowed = allowedResidues(prime)

        if actualNumbers is None:
            nextModulus = modulus * prime
            inverseModulus = pow(modulus, -1, prime)

            if nextModulus <= limit:
                nextResidues = []
                for residue in residues:
                    for targetResidue in allowed:
                        nextResidues.append(
                            combineResidue(
                                residue,
                                modulus,
                                targetResidue,
                                prime,
                                inverseModulus,
                            )
                        )

                residues = nextResidues
                modulus = nextModulus
                currentSurvivors = residueCount(residues, modulus, limit)
            else:
                actualNumbers = []
                for residue in residues:
                    for targetResidue in allowed:
                        number = combineResidue(
                            residue,
                            modulus,
                            targetResidue,
                            prime,
                            inverseModulus,
                        )

                        if 1 <= number <= limit:
                            actualNumbers.append(number)

                residues = None
                modulus = nextModulus
                currentSurvivors = len(actualNumbers)
        else:
            allowedSet = set(allowed)
            actualNumbers = [
                number for number in actualNumbers if number % prime in allowedSet
            ]
            currentSurvivors = len(actualNumbers)

        answer += prime * (previousSurvivors - currentSurvivors)
        previousSurvivors = currentSurvivors

        if currentSurvivors == 0:
            return answer

    raise RuntimeError("Prime generator stopped unexpectedly.")


def solve():
    return U(TARGET)


def runTests():
    assert unluckyPrime(14) == 3
    assert unluckyPrime(147) == 2
    assert unluckyPrime(1470) == 13
    assert U(1470) == 4_293


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
