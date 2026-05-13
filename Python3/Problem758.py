import time
from collections import deque
from math import gcd


MOD = 1_000_000_007


def primeSieve(limit):
    sieve = bytearray(b"\x01") * limit
    sieve[0:2] = b"\x00\x00"
    for n in range(2, int(limit ** 0.5) + 1):
        if sieve[n]:
            start = n * n
            sieve[start:limit:n] = b"\x00" * (((limit - 1 - start) // n) + 1)
    return [n for n in range(limit) if sieve[n]]


def minimalPouringSearch(a, b):
    capacities = (a, b, a + b)
    start = (a, b, 0)
    if 1 in start:
        return 0

    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, distance = queue.popleft()
        for source in range(3):
            if state[source] == 0:
                continue
            for destination in range(3):
                if source == destination or state[destination] == capacities[destination]:
                    continue

                amount = min(state[source], capacities[destination] - state[destination])
                nextState = list(state)
                nextState[source] -= amount
                nextState[destination] += amount
                nextState = tuple(nextState)

                if nextState in seen:
                    continue
                if 1 in nextState:
                    return distance + 1
                seen.add(nextState)
                queue.append((nextState, distance + 1))

    raise ValueError("unreachable state space")


def continuedFractionTerms(numerator, denominator):
    terms = []
    while denominator:
        quotient, remainder = divmod(numerator, denominator)
        terms.append(quotient)
        numerator, denominator = denominator, remainder
    return terms


def penultimateConvergent(terms):
    p2, p1 = 0, 1
    q2, q1 = 1, 0
    convergents = []
    for term in terms:
        p = term * p1 + p2
        q = term * q1 + q2
        convergents.append((p, q))
        p2, p1 = p1, p
        q2, q1 = q1, q
    return convergents[-2] if len(convergents) > 1 else convergents[0]


def minimalPourings(a, b):
    if not (0 < a <= b) or gcd(a, b) != 1:
        raise ValueError("requires coprime positive a <= b")
    if a == 1:
        return 0

    p, q = penultimateConvergent(continuedFractionTerms(b, a))
    return 2 * (p + q) - 2


def geometricSeriesMod(ratio, length, mod):
    ratio %= mod
    if length == 0:
        return 0
    if ratio == 1:
        return length % mod
    return (pow(ratio, length, mod) - 1) * pow(ratio - 1, mod - 2, mod) % mod


def mersenneContinuedFractionTerms(exponentSmall, exponentLarge, mod):
    terms = []
    high, low = exponentLarge, exponentSmall
    while True:
        quotient, remainder = divmod(high, low)
        ratio = pow(2, low, mod)
        shift = pow(2, remainder, mod)
        terms.append(shift * geometricSeriesMod(ratio, quotient, mod) % mod)

        if remainder == 0:
            return terms
        high, low = low, remainder


def penultimateConvergentMod(terms, mod):
    p2, p1 = 0, 1
    q2, q1 = 1, 0
    previous = None
    current = None
    for term in terms:
        p = (term * p1 + p2) % mod
        q = (term * q1 + q2) % mod
        previous, current = current, (p, q)
        p2, p1 = p1, p
        q2, q1 = q1, q
    return previous if previous is not None else current


def mersennePouringCountMod(exponentSmall, exponentLarge, mod=MOD):
    terms = mersenneContinuedFractionTerms(exponentSmall, exponentLarge, mod)
    p, q = penultimateConvergentMod(terms, mod)
    return (2 * (p + q) - 2) % mod


def solve():
    primes = primeSieve(1000)
    exponents = [prime ** 5 for prime in primes]
    total = 0
    for i, exponentSmall in enumerate(exponents):
        for exponentLarge in exponents[i + 1:]:
            total += mersennePouringCountMod(exponentSmall, exponentLarge)
    return total % MOD


def runTests():
    assert minimalPourings(3, 5) == 4
    assert minimalPourings(7, 31) == 20
    assert minimalPourings(1234, 4321) == 2780

    for a in range(2, 10):
        for b in range(a, 20):
            if gcd(a, b) == 1:
                assert minimalPourings(a, b) == minimalPouringSearch(a, b)

    assert mersennePouringCountMod(2, 3) == minimalPourings(3, 7)
    assert mersennePouringCountMod(3, 5) == minimalPourings(7, 31)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
