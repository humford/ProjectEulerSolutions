import collections
import math
import time


def primesUpTo(limit):
    primes = []
    for n in range(2, limit + 1):
        if all(n % factor for factor in range(2, math.isqrt(n) + 1)):
            primes.append(n)
    return primes


def primeExponent(n, prime):
    exponent = 0
    while n % prime == 0:
        exponent += 1
        n //= prime
    return exponent


def reducedCandidates(limit):
    candidates = set(range(2, limit + 1))
    primes = primesUpTo(limit)
    changed = True

    while changed:
        changed = False
        for prime in primes:
            if prime == 2:
                continue

            max_exponent = max((primeExponent(n, prime) for n in candidates), default=0)
            for exponent in range(max_exponent, 0, -1):
                group = [n for n in candidates if primeExponent(n, prime) == exponent]
                if not group:
                    continue

                modulus = prime * prime
                coefficients = []
                for n in group:
                    reduced = n // (prime ** exponent)
                    coefficients.append(pow((reduced * reduced) % modulus, -1, modulus))

                allowed = set()
                for mask in range(1 << len(group)):
                    total = sum(
                        coefficients[index]
                        for index in range(len(group))
                        if mask & (1 << index)
                    )
                    if total % modulus == 0:
                        for index, n in enumerate(group):
                            if mask & (1 << index):
                                allowed.add(n)

                removed = [n for n in group if n not in allowed]
                if removed:
                    candidates.difference_update(removed)
                    changed = True

    return sorted(candidates)


def scaledSubsetSums(values, scale, target):
    sums = collections.Counter({0: 1})

    for n in values:
        weight = scale // (n * n)
        additions = collections.Counter()
        for current, count in sums.items():
            next_sum = current + weight
            if next_sum <= target:
                additions[next_sum] += count
        sums.update(additions)

    return sums


def reciprocalSquareWays(limit):
    candidates = reducedCandidates(limit)
    scale = 1
    for n in candidates:
        scale = math.lcm(scale, n * n)

    target = scale // 2
    middle = len(candidates) // 2
    left_sums = scaledSubsetSums(candidates[:middle], scale, target)
    right_sums = scaledSubsetSums(candidates[middle:], scale, target)

    return sum(count * right_sums.get(target - value, 0) for value, count in left_sums.items())


def runTests():
    candidates = reducedCandidates(80)
    assert 11 not in candidates
    assert 80 in candidates


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = reciprocalSquareWays(80)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
