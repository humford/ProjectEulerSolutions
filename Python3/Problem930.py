from math import cos, factorial, fsum, pi
import time


TARGET_N = 12
TARGET_M = 12


def spectralCosines(n):
    return [cos(2 * pi * residue / n) for residue in range(n)]


def F(n, m):
    # Work with labeled balls and quotient by a common rotation.  The relative
    # position chain is a random walk on (Z/nZ)^(m-1), started from stationarity,
    # and stopping means hitting the origin.  For a transitive reversible chain,
    # this stationary hitting time is sum 1/(1-lambda) over nontrivial
    # eigenvalues.
    #
    # Characters can be represented as m residues k_i with sum k_i = 0 mod n.
    # The eigenvalue is average(cos(2*pi*k_i/n)).  We group equal residues by
    # counts to avoid summing n^(m-1) terms directly.
    cosines = spectralCosines(n)
    factorials = [factorial(i) for i in range(m + 1)]
    counts = [0] * n
    terms = []

    def search(residue, remaining, residueSum, cosineSum, denominator):
        if residue == n - 1:
            count = remaining
            counts[residue] = count
            totalResidue = (residueSum + residue * count) % n

            if totalResidue == 0 and counts[0] != m:
                multiplicity = factorials[m] // (denominator * factorials[count])
                eigenvalue = (cosineSum + cosines[residue] * count) / m
                terms.append(multiplicity / (1 - eigenvalue))

            counts[residue] = 0
            return

        for count in range(remaining + 1):
            counts[residue] = count
            search(
                residue + 1,
                remaining - count,
                (residueSum + residue * count) % n,
                cosineSum + cosines[residue] * count,
                denominator * factorials[count],
            )

        counts[residue] = 0

    search(0, m, 0, 0.0, 1)
    return fsum(terms)


def G(n, m):
    return fsum(
        F(bowls, balls)
        for bowls in range(2, n + 1)
        for balls in range(2, m + 1)
    )


def scientificFormat(value):
    mantissa, exponent = f"{value:.12e}".split("e")
    return mantissa + "e" + str(int(exponent))


def solve():
    return scientificFormat(G(TARGET_N, TARGET_M))


def runTests():
    assert abs(F(2, 2) - 1 / 2) < 1e-12
    assert abs(F(3, 2) - 4 / 3) < 1e-12
    assert abs(F(2, 3) - 9 / 4) < 1e-12
    assert abs(F(4, 5) - 6875 / 24) < 1e-9
    assert abs(G(3, 3) - 137 / 12) < 1e-10
    assert abs(G(4, 5) - 6277 / 12) < 1e-9
    assert scientificFormat(G(6, 6)) == "1.681521567954e4"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
