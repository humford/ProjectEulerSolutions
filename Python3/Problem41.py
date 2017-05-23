import time
from itertools import permutations

#AKS Primality Test
#https://en.wikipedia.org/wiki/AKS_primality_test
#Python implementation from: https://stackoverflow.com/questions/1801391/what-is-the-best-algorithm-for-checking-if-a-number-is-prime
def isprime(n):
    """Returns True if n is prime."""
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True

def largestPandigitalPrime():
 	largestpd = 0
 	for m in range(4, 10):
 		test = permutations("".join([str(d) for d in range(1, m+1)]))
 		for pandigital in test:
 			pd = int("".join(pandigital))
 			if pd > largestpd:
 				if isprime(pd):
 					largestpd = pd
 	return largestpd


start = time.time()
answer = largestPandigitalPrime()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")