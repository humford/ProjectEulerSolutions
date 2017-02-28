import math


def s(i):
    for m in range(1, i + 1):
        if math.factorial(m) % i == 0:
            return m


def S(n):
    z = 0
    for i in range(2, n + 1):
        z += s(i)
    return z


print(S(10 ** 8))
