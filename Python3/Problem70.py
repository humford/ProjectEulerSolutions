import time
from array import array


def totientSieve(limit):
    totients = array("I", range(limit))

    for n in range(2, limit):
        if totients[n] == n:
            for multiple in range(n, limit, n):
                totients[multiple] -= totients[multiple] // n

    return totients


def arePermutations(a, b):
    return sorted(str(a)) == sorted(str(b))


def minimumTotientPermutation(limit):
    totients = totientSieve(limit)
    best_n = None
    best_phi = None

    for n in range(2, limit):
        phi = totients[n]
        if arePermutations(n, phi) and (
            best_n is None or n * best_phi < best_n * phi
        ):
            best_n = n
            best_phi = phi

    return best_n


def runTests():
    totients = totientSieve(11)
    assert [totients[n] for n in range(2, 11)] == [1, 2, 2, 4, 2, 6, 4, 6, 4]
    assert arePermutations(87109, 79180)
    assert minimumTotientPermutation(100) == 21


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = minimumTotientPermutation(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
