import time
import math

def numberOfDivisors(n):
	nod = 0
	sqrt = int(math.sqrt(n))

	for i in range(1, sqrt):
		if n % i == 0:
			nod += 2

	if sqrt ** 2 == n:
		nod -= 1

	return nod

def triangleNumber(d=500):
	n = 0
	i = 1
	while numberOfDivisors(n) < d:
		n += i
		i += 1
	return n

start = time.time()
trianglenum = triangleNumber(int(raw_input("Number of Divisors: ")))
elapsed = (time.time() - start)

print "found %s in %s seconds" % (trianglenum, elapsed)