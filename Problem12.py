import time
import math

def ASieve(limit):
	is_prime = list()
	is_prime = [False] * (limit+1)
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
	return is_prime

def listPrimes(limit):
	primes = [2,3]
	is_prime = ASieve(limit)
	for n in range(5, limit):
		if is_prime[n]: primes.append(n)
	return primes

def numberOfDivisors(n):
	nod = 0
	sqrt = int(math.sqrt(n))

	for i in range(1, sqrt):
		if n % i == 0:
			nod += 2

	if sqrt ** 2 == n:
		nod -= 1

	return nod

def primeFactorisationNoD(n, primelist=listPrimes(75000)):
	nod = 1
	remain = n
	for i in range(0, len(primelist)):
		if primelist[i] * primelist[i] > n:
			return nod*2
		exponent = 1
		while remain % primelist[i] == 0:
			exponent += 1
			remain = remain/primelist[i]
		nod *= exponent
		if remain == 1:
			return nod
	return nod

def triangleNumber(d=500):
	n = 0
	i = 1
	while primeFactorisationNoD(n) < d:
		n += i
		i += 1
	return n

start = time.time()
trianglenum = triangleNumber(int(raw_input("Number of Divisors: ")))
elapsed = (time.time() - start)

print "found %s in %s seconds" % (trianglenum, elapsed)