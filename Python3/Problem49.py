from itertools import combinations


def primeSieve(limit):
    is_prime = [True] * limit
    is_prime[0] = False
    is_prime[1] = False

    for value in range(2, int(limit ** 0.5) + 1):
        if is_prime[value]:
            for multiple in range(value * value, limit, value):
                is_prime[multiple] = False

    return is_prime


def primePermutationSequences():
    primes = primeSieve(10000)
    groups = {}

    for value in range(1000, 10000):
        if primes[value]:
            key = "".join(sorted(str(value)))
            groups.setdefault(key, []).append(value)

    sequences = []
    for group in groups.values():
        prime_set = set(group)
        for first, second in combinations(group, 2):
            third = second + (second - first)
            if third in prime_set:
                sequences.append((first, second, third))

    return sequences


def solve():
    for sequence in primePermutationSequences():
        if sequence != (1487, 4817, 8147):
            return "".join(str(value) for value in sequence)
    raise ValueError("No second sequence found")


def runTests():
    assert (1487, 4817, 8147) in primePermutationSequences()


if __name__ == "__main__":
    runTests()
    print(solve())
