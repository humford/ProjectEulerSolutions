import math
import time


def ASieve(limit):
    is_prime = [False] * (limit + 1)

    for x in range(1, int(math.sqrt(limit)) + 1):
        for y in range(1, int(math.sqrt(limit)) + 1):

            n =  4 * x ** 2 + y ** 2
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

    if len(is_prime) > 4:
        is_prime[2] = True
        is_prime[3] = True

    return is_prime

def isGoldbach(n, primes):
    goldbach = None;
    for prime in range(0, len(primes)):
        if primes[prime] and n - prime > 0:
            nonprimepart = n - prime
            square = nonprimepart / 2.0
            if (math.sqrt(square)).is_integer():
                print(str(n) + " = " + str(prime) + " + 2x" + str(int(math.sqrt(square))) + "^2")
                goldbach = True
            elif goldbach != True:
                goldbach = False
        elif n - prime < 0:
            break
    return goldbach

def findSmallestNonGoldbach(limit):
    primes = ASieve(limit)
    for composite in range(5, len(primes)):
        if not primes[composite] and not composite % 2 == 0:
            if not isGoldbach(composite, primes):
                return composite
    return "Non-Goldbach not found"

start = time.time()
answer = findSmallestNonGoldbach(10000)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
