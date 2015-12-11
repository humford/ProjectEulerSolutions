def sumMultiples(x,y,range):
	m = []
	for i in xrange(1,range):
		if i % x == 0 or i % y == 0:
			m.append(i)
	print m
	return sum(m)

print sumMultiples(3,5,1000)