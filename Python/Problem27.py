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

primelist = ASieve(100000)

def primeTest(p):
	# if p % 2 == 0:
	# 	return False
	# elif p % 5 == 2 or p % 5 == -2:
	# 	if (2 ** (p-1)) % p == 1 and fibonacci((p+1)) % p == 0:
	# 		return True
	# return False
	return primelist[p]


def testPrimeGenerator(a, b):
	n = 0
	x = n**2 + a*n + b
	while(primeTest(x)):
		x = n**2 + a*n + b
		n += 1
	return n

def testGenerators(r):
	top = 0
	coef = []
	for a in range(-r, r):
		for b in range(-r, r):
			test = testPrimeGenerator(a,b)
			if test > top:
				top = test
				coef = [a,b]
	return coef, top

print(testGenerators(1000))
