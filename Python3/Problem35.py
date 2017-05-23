import time
import math
from itertools import permutations

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

def isCircular(n, primes):
	nlist = [int(digit) for digit in str(n)]
	rotations = []
	for position in range(0, len(nlist)):
		rotations.append(nlist[position:] + nlist[:position])
	for rotation in rotations:
		if not primes[int("".join([str(x) for x in rotation]))]:
			return False
	return True

def circularPrimesBelow(limit):
	primes = ASieve(limit)
	circularPrimes = []
	for number in range(0, len(primes)):
		if primes[number] and isCircular(number, primes):
			circularPrimes.append(number)
	return circularPrimes

start = time.time()
answer = circularPrimesBelow(1000000)
elapsed = (time.time() - start)

print("Found " + str(len(answer)) + " in " + str(elapsed) + " seconds.")