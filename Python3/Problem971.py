from math import isqrt
import time


TARGET = 10**8


def sievePrimesUpTo(limit):
    if limit < 2:
        return []

    sieve = bytearray((limit // 2) + 1)
    root = isqrt(limit)
    for index in range(1, root // 2 + 1):
        if sieve[index] == 0:
            prime = 2 * index + 1
            start = (prime * prime - 1) // 2
            sieve[start::prime] = b"\x01" * ((len(sieve) - 1 - start) // prime + 1)

    primes = [2]
    primes.extend(
        2 * index + 1
        for index, value in enumerate(sieve)
        if index > 0 and value == 0 and 2 * index + 1 <= limit
    )
    return primes


def periodicCountInFifthRoots(prime):
    exponent = (prime - 1) // 5
    generator = 2
    zeta = pow(generator, exponent, prime)
    while zeta == 1:
        generator += 1
        zeta = pow(generator, exponent, prime)

    roots = [1]
    current = 1
    for _ in range(4):
        current = current * zeta % prime
        roots.append(current)

    image = {}
    for root in roots:
        image[root] = root * pow((1 + root) % prime, exponent, prime) % prime

    visited = {}
    inCycle = set()
    for root in roots:
        if root in visited:
            continue

        path = []
        current = root
        while True:
            if current not in visited:
                visited[current] = 1
                path.append(current)
                current = image.get(current)
                if current is None:
                    for value in path:
                        visited[value] = 2
                    break
            elif visited[current] == 1:
                cycleStart = path.index(current)
                inCycle.update(path[cycleStart:])
                for value in path:
                    visited[value] = 2
                break
            else:
                for value in path:
                    visited[value] = 2
                break

    return len(inCycle)


def C(prime):
    if prime % 5 != 1:
        return 0
    return 1 + ((prime - 1) // 5) * periodicCountInFifthRoots(prime)


def S(limit):
    total = 0
    for prime in sievePrimesUpTo(limit):
        if prime % 5 == 1:
            total += C(prime)
    return total


def solve():
    return S(TARGET)


def runTests():
    assert C(11) == 7
    assert S(100) == 127


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
