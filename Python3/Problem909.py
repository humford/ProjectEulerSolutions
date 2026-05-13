import time


MODULUS = 1_000_000_000


def zero(function):
    return lambda value: value


def successor(numeral):
    return lambda function: lambda value: function(numeral(function)(value))


def a(value):
    return value + 1


def z(u):
    return lambda v: v


def s(u):
    return lambda v: lambda w: v(u(v)(w))


def bTransform(n):
    return n * (n + 1)


def fTransform(n):
    h = n * n * (n + 1)
    return h * (h + 1)


def targetCount():
    one = 1
    six = fTransform(one)
    fortyTwo = bTransform(six)
    return bTransform(fTransform(fortyTwo))


def solve():
    return targetCount() % MODULUS


def runTests():
    assert zero(a)(0) == 0
    assert successor(zero)(a)(0) == 1

    directI = s(z)
    directB = s(s)
    directF = directB(directB)
    directH = s(directB)(directB)

    assert directI(a)(0) == 1
    assert directF(directI)(a)(0) == 6
    assert directH(directI)(a)(0) == 42

    assert s(z)(a)(0) == 1
    assert s(s)(s(s))(s(z))(a)(0) == 6
    assert solve() == 399_885_292


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer).zfill(9) + " in " + str(elapsed) + " seconds.")
