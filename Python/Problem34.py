import math

def digitFactorialSum(n):
	m = [math.factorial(int(x)) for x in str(n)]
	return sum(m)

def findDFSUnder(max):
	dfs = []
	for x in range(3, max+1):
		if digitFactorialSum(x) == x:
			dfs.append(x)
	return dfs

print sum(findDFSUnder(1000000))