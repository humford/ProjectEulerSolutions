import math
import time

def isPseudoPrime(n):
    if n <= 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    elif n < 9:
        return True
    elif n % 3 == 0:
        return False
    elif n % 5 == 0:
        return False
    ar = [2,3]
    for i in range(len(ar)):
        if witness(ar[i], n):
            return False
    return True

def witness(a, n):
    t = 0
    u = n - 1
    while (u & 1) == 0:
        t += 1
        u >>= 1

    xi1 = modularExp(a, u, n)
    xi2 = 0

    for i in range(t):
        xi2 = xi1 * xi1 % n
        if (xi2 == 1) and (xi1 != 1) and (xi1 != (n - 1)):
            return True
        xi1 = xi2

    return xi1 != 1

def modularExp(a, b, n):
    d = 1
    k = 0
    while ((b >> k) > 0):
        k += 1
    for i in range(k-1, -1, -1):
        d = d * d % n
        if ((b >> i) & 1) > 0:
            d = d * a % n
    return d

def spiralprimes(prob):
    prime_count = 3
    sl = 2
    c = 9
    while prime_count / (2*sl+1) > prob:
        sl += 2
        for i in range(3):
            c += sl
            if isPseudoPrime(c):
                prime_count += 1
        c += sl
    return sl + 1

start = time.time()
answer = spiralprimes(0.10)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
