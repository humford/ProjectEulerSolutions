import time
from array import array


LIMIT = 20_000_000
MODULUS = 10**8


def totients(limit):
    phi = array("I", range(limit + 1))

    for prime in range(2, limit + 1):
        if phi[prime] == prime:
            for multiple in range(prime, limit + 1, prime):
                phi[multiple] -= phi[multiple] // prime

    return phi


class Fenwick:
    def __init__(self, size, modulus):
        self.size = size
        self.modulus = modulus
        self.tree = array("I", [0]) * (size + 2)

    def add(self, index, value):
        while index <= self.size:
            self.tree[index] = (self.tree[index] + value) % self.modulus
            index += index & -index

    def rangeAdd(self, left, right, value):
        if left > right:
            return

        self.add(left, value)
        self.add(right + 1, (-value) % self.modulus)

    def query(self, index):
        total = 0

        while index > 0:
            total = (total + self.tree[index]) % self.modulus
            index -= index & -index

        return total


def totientStairstepCount(limit=LIMIT, modulus=MODULUS):
    phi = totients(limit)
    fenwick = Fenwick(limit + 1, modulus)
    total = 0

    for value in range(1, limit + 1):
        sequenceCount = fenwick.query(phi[value])

        if value == 6:
            sequenceCount = (sequenceCount + 1) % modulus

        total = (total + sequenceCount) % modulus

        if sequenceCount:
            fenwick.rangeAdd(phi[value] + 1, value - 1, sequenceCount)

    return total


def runTests():
    assert totientStairstepCount(10) == 4
    assert totientStairstepCount(100) == 82073668
    assert totientStairstepCount(10000) == 73808307


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totientStairstepCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
