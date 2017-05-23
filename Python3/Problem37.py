import time
import math

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

def isTruncatable(n, primes):
	for p in range(1, len(str(n))):
		if not primes[int(n % 10 ** p)]:
			return False
	for p in range(1, len(str(n))):
		if not primes[int(n / 10 ** p)]:
			return False
	return True

def truncatablePrimes(limit):
	primes = ASieve(limit)
	tprimes = []
	for prime in range(8, len(primes)):
		if primes[prime] and isTruncatable(prime, primes):
			tprimes.append(prime)
	return tprimes

start = time.time()
answer = truncatablePrimes(1000000)
elapsed = (time.time() - start)

print("Found " + str(sum(answer)) + " in " + str(elapsed) + " seconds.")