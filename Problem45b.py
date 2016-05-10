import math

def testPentagonal(n):
	n = float(n)
	n = (math.sqrt(24*n+1)+1)/6
	print n
	return n.is_integer()

result = long(0)
i = int(143)

while (True):
	i += 1
	result = i * (2 * i - 1)

	if testPentagonal(result):
		break

print result
#1533776805