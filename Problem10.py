import math
import time

def sumPrimesBelow(limit):
	is_prime = list()
	is_prime = [False] * (limit+1)

	s = 0

	for x in range(1, int(math.sqrt(limit))+1):
		for y in range(1, int(math.sqrt(limit))+1):
			
			n = 4*x**2 + y**2
			if n <= limit and (n%12==1 or n%12==5):
				is_prime[n] = not is_prime[n]

			n = 3*x**2+y**2
			if n <= limit and n%12==7:
				is_prime[n] = not is_prime[n]

			n = 3*x**2-y**2
			if x > y and n <= limit and n%12==11:
				is_prime[n] = not is_prime[n]

	for n in range(5, int(math.sqrt(limit))):
		if is_prime[n]:
			for k in range(n**2, limit+1, n**2):
				is_prime[k] = False

	s += 2
	s += 3
	for n in range(5, limit):
		if is_prime[n]: s += n

	return s

start = time.time()
prime = sumPrimesBelow(int(raw_input("Number: ")))
elapsed = (time.time() - start)

print "found %s in %s seconds" % (prime, elapsed)