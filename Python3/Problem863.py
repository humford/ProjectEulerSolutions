import time


DICE = (5, 6)
EPSILON = 1e-13


def R(n):
    values = [0.0] * n

    for _ in range(100000):
        delta = 0.0

        for state in range(n - 1, 0, -1):
            best = float("inf")

            for die in DICE:
                nextState = (state * die) % n
                if nextState == 0:
                    cost = 1.0
                else:
                    cost = 1.0 + nextState / (state * die) * values[nextState]
                best = min(best, cost)

            delta = max(delta, abs(best - values[state]))
            values[state] = best

        if delta < EPSILON:
            return values[1]

    raise RuntimeError("R({}) did not converge".format(n))


def S(n):
    return sum(R(k) for k in range(2, n + 1))


def runTests():
    assert abs(R(8) - 2.0833333333333335) < 1e-12
    assert abs(R(28) - 2.1424761904761907) < 1e-12
    assert round(S(30), 6) == 56.054622


def solve():
    return "{:.6f}".format(S(1000))


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
