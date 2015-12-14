import time

def findPythTriplet(n):
	a = 0
	b = 0
	c = 0
	for x in range(1,n+1):
		a = x
		for y in range(a+1,n+1):
			b = y
			for z in range(b+1,n+1):
				c = z
				if a**2 + b**2 == c**2:
					if a + b + c == n:
						print a, b, c
						return a * b * c
	pass


start = time.time()
product = findPythTriplet(int(raw_input("a + b + c = ")))
elapsed = (time.time() - start)

print "found %s in %s seconds" % (product, elapsed)