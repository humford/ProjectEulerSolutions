import time


REQUIRED_OFFSETS = (1, 3, 7, 9, 13, 27)
FORBIDDEN_OFFSETS = (5, 11, 15, 17, 19, 21, 23, 25)


def isPrime(n):
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for base in small_primes:
        if base >= n:
            continue
        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def allowedResidues():
    residues = [0]
    modulus = 10

    for prime in (7, 11, 13, 17, 19, 23):
        next_residues = []
        for residue in residues:
            for offset in range(prime):
                candidate = residue + modulus * offset
                square = candidate * candidate
                if all((square + required) % prime != 0 for required in REQUIRED_OFFSETS):
                    next_residues.append(candidate)
        residues = next_residues
        modulus *= prime

    return modulus, residues


def hasPrimePattern(n):
    square = n * n
    return all(isPrime(square + offset) for offset in REQUIRED_OFFSETS) and all(
        not isPrime(square + offset) for offset in FORBIDDEN_OFFSETS
    )


def primePatternSum(limit):
    modulus, residues = allowedResidues()
    total = 0

    for residue in residues:
        n = residue
        while n < limit:
            if n > 0 and hasPrimePattern(n):
                total += n
            n += modulus

    return total


def runTests():
    assert hasPrimePattern(10)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = primePatternSum(150000000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
