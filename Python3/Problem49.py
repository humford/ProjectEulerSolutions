import math
import time
from itertools import permutations, groupby

def sum_digits3(n):
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r


def ASieve(limit):
    is_prime = [False] * (limit + 1)

    for x in range(1, int(math.sqrt(limit)) + 1):
        for y in range(1, int(math.sqrt(limit)) + 1):

            n = 4 * x ** 2 + y ** 2
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                is_prime[n] = not is_prime[n]

            n = 3 * x ** 2 + y ** 2
            if n <= limit and n % 12 == 7:
                is_prime[n] = not is_prime[n]

            n = 3 * x ** 2 - y ** 2
            if x > y and n <= limit and n % 12 == 11:
                is_prime[n] = not is_prime[n]

    for n in range(5, int(math.sqrt(limit))):
        if is_prime[n]:
            for k in range(n ** 2, limit + 1, n ** 2):
                is_prime[k] = False

    return is_prime


def find4digprimes():
    r = ASieve(10000)
    result = []
    for x in range(1000, len(r)):
        if r[x]:
            result.append(x)
    return result


def findArith():
    r = find4digprimes()
    possible = []
    for prime in r:
        plist = []
        for p in permutations(str(prime)):
            t = int("".join(p)) in r
            if int("".join(p)) in r:
                plist.append(int("".join(p)))
        if plist:
            possible.append(sorted(list(set(plist))))
    solutions = []
    for p in possible:
        gaps = []
        for n in range(len(p)-1):
            gaps.append(p[n+1] - p[n])
        if any(sum(1 for _ in g) > 1 for _, g in groupby(gaps)):
            solutions.append(p)
    return solutions

start = time.time()
answer = findArith()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
