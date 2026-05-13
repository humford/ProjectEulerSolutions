from math import gcd
import time


TARGET = 10**12 + 39


def isPrime(value):
    if value < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if value % prime == 0:
            return value == prime

    oddPart = value - 1
    twoPower = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        twoPower += 1

    for base in (2, 3, 5, 7, 11, 13):
        if base >= value:
            continue
        current = pow(base, oddPart, value)
        if current == 1 or current == value - 1:
            continue
        for _ in range(twoPower - 1):
            current = (current * current) % value
            if current == value - 1:
                break
        else:
            return False
    return True


def modularInverse(value, modulus):
    value %= modulus
    x, y = value, modulus
    vx, vy = 1, 0

    while x:
        quotient = y // x
        y %= x
        vy -= quotient * vx
        x, y = y, x
        vx, vy = vy, vx

    if y != 1:
        return None
    return vy % modulus


def f(n):
    """Return the smallest coprime m giving minimal subtractive Euclid labour.

    The search walks the Euclid/Stern-Brocot tree by total subtraction count and
    splits each candidate path near the middle. The second half is recovered by
    a short lattice reduction, then the symmetry orbit
    {m, n-m, m^{-1}, n-m^{-1}} is minimized. The symmetry is valid for the
    prime moduli used in the statement checks and target.
    """
    if not isPrime(n):
        raise ValueError("This search routine is intended for prime n.")

    steps = 0

    while True:
        bestSteps = steps
        bestValue = n + 1
        midpoint = (steps + 1) // 2

        def search(a, b, ca, cb, depth):
            nonlocal bestSteps, bestValue

            if a > b:
                a, b = b, a
                ca, cb = cb, ca

            if cb < 0:
                return
            if ca < 0:
                shift = (-ca + b - 1) // b
                ca += shift * b
                cb -= shift * a
                if cb < 0:
                    return

            if a * ca + b * cb != n:
                return

            if depth == midpoint:
                localA, localB = a, b
                localCA, localCB = ca, cb

                if steps % 2:
                    localA *= 2
                    localB *= 2
                    localCA *= 2
                    localCB *= 2
                    localB -= localA // 2
                    localCA += localCB // 2
                    if localA * localCA + localB * localCB != 4 * n:
                        return

                norm = localA * localA + localB * localB
                if norm < n:
                    return

                cross = localCA * localB - localCB * localA
                quotient = cross // norm
                localCA -= quotient * localB
                localCB += quotient * localA
                cross -= quotient * norm

                if cross < 0:
                    localCA += localB
                    localCB -= localA

                def check(candidateA, candidateB):
                    nonlocal bestSteps, bestValue

                    if candidateA < 0 or candidateB < 0:
                        return
                    if candidateA * candidateA + candidateB * candidateB > norm:
                        return

                    x, y = candidateA, candidateB
                    vx, vy = localA, localB

                    if steps % 2:
                        if vx % 2 or y % 2:
                            return
                        x -= y // 2
                        vy += vx // 2
                        if vy % 2 or x % 2:
                            return
                        x //= 2
                        y //= 2
                        vx //= 2
                        vy //= 2

                    if x * vx + y * vy != n:
                        return

                    operations = 0
                    while operations <= steps - midpoint and x and y:
                        if x > y:
                            x, y = y, x
                            vx, vy = vy, vx
                        y -= x
                        vx += vy
                        operations += 1

                    if operations > steps - midpoint:
                        return

                    representative = (vx + vy - n) % n
                    inverse = modularInverse(representative, n)
                    if inverse is None:
                        return

                    candidateSteps = depth + operations
                    candidateValue = min(
                        representative,
                        n - representative,
                        inverse,
                        n - inverse,
                    )

                    if (
                        candidateSteps < bestSteps
                        or candidateSteps == bestSteps
                        and candidateValue < bestValue
                    ):
                        bestSteps = candidateSteps
                        bestValue = candidateValue

                check(localCA, localCB)
                check(localCA - localB, localCB + localA)
                return

            x, y = a, b
            for _ in range(depth, steps // 2):
                if x > y:
                    x, y = y, x
                x += y
                x, y = y, x
            if x > y:
                x, y = y, x

            if steps % 2:
                if 5 * y * y // 4 + x * y + x * x < n:
                    return
            else:
                if x * x + y * y < n:
                    return

            search(b, a + b, cb - ca, ca, depth + 1)
            if 0 < a < b:
                search(a, a + b, ca - cb, cb, depth + 1)

        search(0, 1, 0, n, 0)

        if bestValue <= n:
            return bestValue
        steps += 1


def subtractionSteps(a, b):
    steps = 0
    while a != b:
        if a < b:
            a, b = b, a
        a -= b
        steps += 1
    return steps


def bruteF(n):
    bestSteps = None
    bestValue = None
    for m in range(1, n):
        if gcd(n, m) != 1:
            continue
        steps = subtractionSteps(n, m)
        if bestSteps is None or steps < bestSteps:
            bestSteps = steps
            bestValue = m
    return bestValue


def solve():
    return f(TARGET)


def runTests():
    assert isPrime(TARGET)
    assert f(7) == 2
    assert f(89) == 34
    assert f(8191) == 1_856
    for n in range(2, 40):
        if isPrime(n):
            assert f(n) == bruteF(n)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
