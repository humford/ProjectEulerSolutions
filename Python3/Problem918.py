from functools import lru_cache
import time


TARGET_N = 10**12


@lru_cache(maxsize=None)
def sequenceTriple(n):
    if n == 1:
        return 1, 2, 1

    m = n // 2
    aM, aMPlusOne, _ = sequenceTriple(m)

    if n % 2 == 0:
        return (
            2 * aM,
            aM - 3 * aMPlusOne,
            4 - aM,
        )

    return (
        aM - 3 * aMPlusOne,
        2 * aMPlusOne,
        4 - 3 * aMPlusOne,
    )


def a(n):
    return sequenceTriple(n)[0]


def S(n):
    return sequenceTriple(n)[2]


def solve():
    return S(TARGET_N)


def runTests():
    assert [a(n) for n in range(1, 11)] == [
        1,
        2,
        -5,
        4,
        17,
        -10,
        -17,
        8,
        -47,
        34,
    ]
    assert S(10) == -13
    assert solve() == -6_999_033_352_333_308


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
