import math
import time

def nth_prime(n):
	lst = list(range(2, int(math.ceil(n*math.log(n*math.log(n))))))
	primes = []
	while len(primes) <= n:
		p = lst[0]
		primes.append(p)
		lst = [i for i in lst if i % p != 0]
	return primes[n-1]

start = time.time()
prime = nth_prime(int(raw_input("Number: ")))
elapsed = (time.time() - start)

print "found %s in %s seconds" % (prime, elapsed)