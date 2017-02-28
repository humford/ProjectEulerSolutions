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

def primesBelow(limit):
	l = ASieve(limit)
	f = [1, 2, 3]
	for x in range(0,len(l)):
		if l[x]:
			f.append(x)
	return f

def compositeBelow(limit):
	l = ASieve(limit)
	f = []
	for x in range(4,len(l)):
		if l[x] == False:
			f.append(x)
	return f

def golbachTest(n):
	t = primesBelow(n)
	for x in t:
		if (math.sqrt((float(n) % float(x))/2.0)).is_integer():
			return True
	return False

for n in compositeBelow(100000):
	if not golbachTest(n):
		print n

